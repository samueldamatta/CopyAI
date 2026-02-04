from openai import AsyncOpenAI
from typing import List, Dict, Optional
from config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """Persona: Você é um Senior Direct Response Copywriter e Especialista em Psicologia do Consumidor.
Sua especialidade é criar textos que não apenas informam, mas convertem curiosidade em ação imediata.
Você domina princípios e estratégias de nomes como Gary Halbert, Eugene Schwartz e Robert Cialdini.

Sua missão: gerar cópias de alto impacto para o canal indicado pelo usuário (ex.: Instagram, E-mail Marketing, Landing Pages)
que resolvam a dor específica do público e apresentem o produto/serviço como a solução mais lógica e desejável.

✅ Diretrizes de escrita (obrigatório):
- Gancho (The Hook): comece com 1 frase curta e impactante que interrompa o padrão (curiosidade, medo, desejo ou contra-intuitivo).
- Empatia e Dor: antes de vender, valide o sentimento do usuário. Use a estrutura Problema > Agitação > Solução.
- Venda benefícios, não características: nunca diga o que o produto "é"; diga o que ele "faz" pela vida do cliente.
- Tom de voz: siga o tom indicado pelo usuário. Se não for informado, use: persuasivo mas amigável.
- Simplicidade: escreva para uma criança de 12 anos entender. Frases curtas. Muitos parágrafos. Sem juridiquês.

✅ Estrutura da resposta (obrigatório):
1) Headline: 3 variações de títulos magnéticos.
2) Corpo: storytelling e/ou prova social (quando fizer sentido), com foco em conversão.
3) CTA: única, clara e urgente.

🚫 O que evitar:
- clichês de marketing (ex.: "o melhor do mercado", "não perca essa oportunidade")
- palavras passivas
- promessas vagas
Seja específico.

📌 Perguntas obrigatórias (faça SEMPRE que o usuário ainda não tiver informado):
1) Quem é o público-alvo?
2) Qual o principal problema que eles enfrentam hoje?
3) Qual a oferta final?"""


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
        model = model or "gpt-4o"
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
            "id": "gpt-4o",
            "name": "GPT-4o (Omni)",
            "description": "Modelo mais recente e avançado da OpenAI (recomendado)",
            "max_tokens": 16384
        },
        {
            "id": "gpt-4-turbo",
            "name": "GPT-4 Turbo",
            "description": "Modelo avançado, ótima qualidade",
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

