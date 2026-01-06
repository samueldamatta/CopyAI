from openai import AsyncOpenAI
from typing import List, Dict, Optional
from config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """Você é um agente especialista em criação de copys (textos publicitários) e marketing digital.
Você ajuda usuários a criar copys persuasivas, envolventes e eficazes para diferentes propósitos:

📱 TIPOS DE COPY:
- anuncios: Anúncios de produtos (Facebook Ads, Google Ads, Instagram Ads)
- redes-sociais: Posts para redes sociais (Instagram, LinkedIn, TikTok, Twitter)
- emails: Emails de marketing (sequências, newsletters, cold emails)
- landing-pages: Landing pages (headlines, CTAs, textos de conversão)
- descricoes-produtos: Descrições de produtos (e-commerce, marketplaces)
- scripts-videos: Scripts para vídeos (YouTube, Reels, Stories, TikTok)
- legendas: Legendas e captions
- sites-blogs: Textos para sites e blogs

⚠️ ATENÇÃO: Quando o usuário especificar o tipo de copy no formato "[Tipo de Copy: tipo]", 
você deve focar especificamente nesse tipo de conteúdo e adaptar sua resposta de acordo.

🎯 CARACTERÍSTICAS DAS SUAS COPYS:
- Persuasivas e focadas em conversão
- Adaptadas ao público-alvo específico
- Com gatilhos mentais apropriados (escassez, urgência, prova social, autoridade)
- Claras, objetivas e fáceis de entender
- Criativas e originais
- Otimizadas para SEO quando relevante
- Alinhadas com a voz da marca

💡 METODOLOGIAS QUE VOCÊ DOMINA:
- AIDA (Atenção, Interesse, Desejo, Ação)
- PAS (Problema, Agitação, Solução)
- BAB (Before, After, Bridge)
- 4 Ps (Promessa, Problema, Prova, Proposta)
- Storytelling
- Copywriting emocional

📋 PROCESSO:
1. Sempre pergunte sobre o contexto quando necessário:
   - Qual é o produto/serviço?
   - Quem é o público-alvo? (idade, gênero, interesses, dores)
   - Qual é o objetivo? (vendas, engajamento, tráfego, cadastros)
   - Qual é o tom de voz desejado? (formal, casual, divertido, técnico)
   - Onde será publicado?
   - Há limites de caracteres?

2. Forneça múltiplas opções (2-3 variações) quando relevante
3. Explique o raciocínio por trás das escolhas
4. Sugira melhorias e testes A/B quando apropriado

Seja proativo, criativo e sempre busque a melhor conversão possível!"""


async def generate_copy_response(
    messages: List[Dict[str, str]], 
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None
) -> str:
    """
    Gera uma resposta do agente de IA usando ChatGPT (OpenAI)
    
    Args:
        messages: Lista de mensagens com formato [{"role": "user|assistant", "content": "texto"}]
        model: Modelo a ser usado (padrão: gpt-4-turbo-preview)
                Opções: "gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"
        temperature: Criatividade da resposta (0.0 a 2.0, padrão: 0.7)
                    0.0 = mais determinístico, 1.0 = balanceado, 2.0 = muito criativo
        max_tokens: Número máximo de tokens na resposta (padrão: 2000)
    
    Returns:
        str: Resposta gerada pela IA (ChatGPT)
    """
    try:
        # Configurações padrão
        model = model or "gpt-4-turbo-preview"
        temperature = temperature if temperature is not None else 0.7
        max_tokens = max_tokens or 2000
        
        # Prepara as mensagens com o prompt do sistema
        full_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + messages
        
        print(f"🤖 Chamando ChatGPT ({model})...")
        
        # Chama a API da OpenAI (ChatGPT)
        response = await client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            presence_penalty=0.1,  # Evita repetições
            frequency_penalty=0.1,  # Promove diversidade
        )
        
        ai_response = response.choices[0].message.content
        print(f"✅ ChatGPT respondeu com {len(ai_response)} caracteres")
        
        return ai_response
    
    except Exception as e:
        error_message = str(e)
        print(f"❌ Erro ao chamar ChatGPT: {error_message}")
        
        # Mensagens de erro mais específicas
        if "authentication" in error_message.lower() or "api_key" in error_message.lower():
            return "❌ Erro de autenticação com a API da OpenAI. Verifique sua chave de API no arquivo .env"
        elif "quota" in error_message.lower() or "billing" in error_message.lower():
            return "❌ Limite de uso da API OpenAI atingido. Verifique sua conta em https://platform.openai.com/account/billing"
        elif "rate_limit" in error_message.lower():
            return "⏳ Muitas requisições. Aguarde alguns segundos e tente novamente."
        else:
            return f"❌ Erro ao processar sua solicitação: {error_message}. Tente novamente."


async def generate_conversation_title(first_message: str) -> str:
    """
    Gera um título para a conversa baseado na primeira mensagem usando ChatGPT
    
    Args:
        first_message: Primeira mensagem do usuário
    
    Returns:
        str: Título gerado (máximo 50 caracteres)
    """
    try:
        print(f"🏷️  Gerando título da conversa...")
        
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # Modelo mais rápido e barato para títulos
            messages=[
                {
                    "role": "system",
                    "content": "Gere um título curto (máximo 50 caracteres) e descritivo para uma conversa de criação de copy que começa com a seguinte mensagem. Responda apenas com o título, sem aspas ou pontuação extra."
                },
                {
                    "role": "user",
                    "content": first_message
                }
            ],
            temperature=0.5,
            max_tokens=20,
        )
        
        title = response.choices[0].message.content.strip()
        title = title.replace('"', '').replace("'", '')  # Remove aspas se houver
        final_title = title[:50]  # Limita a 50 caracteres
        
        print(f"✅ Título gerado: {final_title}")
        return final_title
    
    except Exception as e:
        print(f"❌ Erro ao gerar título: {e}")
        return "Nova Conversa"


def get_available_models() -> List[Dict[str, str]]:
    """
    Retorna lista de modelos ChatGPT disponíveis
    
    Returns:
        Lista com informações dos modelos
    """
    return [
        {
            "id": "gpt-4-turbo-preview",
            "name": "GPT-4 Turbo",
            "description": "Modelo mais avançado, melhor qualidade (recomendado para copys profissionais)",
            "max_tokens": 4096
        },
        {
            "id": "gpt-4",
            "name": "GPT-4",
            "description": "Modelo avançado e confiável",
            "max_tokens": 8192
        },
        {
            "id": "gpt-3.5-turbo",
            "name": "GPT-3.5 Turbo",
            "description": "Modelo rápido e econômico (bom para testes)",
            "max_tokens": 4096
        }
    ]

