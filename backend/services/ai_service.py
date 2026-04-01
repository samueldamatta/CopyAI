from agents import Agent, Runner
from typing import List, Dict, Optional

from .ai_agents import COPYWRITER_INSTRUCTIONS, copywriter_agent, title_agent


async def generate_copy_response(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> str:
    try:
        agent = copywriter_agent
        if model and model != "gpt-4o":
            agent = Agent(
                name="Copywriter",
                instructions=COPYWRITER_INSTRUCTIONS,
                model=model,
            )

        print(f"🤖 Chamando agente Copywriter ({agent.model})...")

        result = await Runner.run(agent, input=messages)
        ai_response = result.final_output

        print(f"✅ Agente respondeu com {len(ai_response)} caracteres")
        return ai_response

    except Exception as e:
        error_message = str(e)
        print(f"❌ Erro no agente Copywriter: {error_message}")

        if "authentication" in error_message.lower() or "api_key" in error_message.lower():
            return "❌ Erro de autenticação com a API da OpenAI. Verifique sua chave de API no arquivo .env"
        elif "quota" in error_message.lower() or "billing" in error_message.lower():
            return "❌ Limite de uso da API OpenAI atingido. Verifique sua conta em https://platform.openai.com/account/billing"
        elif "rate_limit" in error_message.lower():
            return "⏳ Muitas requisições. Aguarde alguns segundos e tente novamente."
        else:
            return f"❌ Erro ao processar sua solicitação: {error_message}. Tente novamente."


async def generate_conversation_title(first_message: str) -> str:
    try:
        print(f"🏷️  Gerando título da conversa...")

        result = await Runner.run(title_agent, first_message)
        title = result.final_output.strip().replace('"', '').replace("'", "")
        final_title = title[:50]

        print(f"✅ Título gerado: {final_title}")
        return final_title

    except Exception as e:
        print(f"❌ Erro ao gerar título: {e}")
        return "Nova Conversa"


def get_available_models() -> List[Dict[str, str]]:
    return [
        {
            "id": "gpt-4o",
            "name": "GPT-4o (Omni)",
            "description": "Modelo mais recente e avançado da OpenAI (recomendado)",
            "max_tokens": 16384,
        },
        {
            "id": "gpt-4-turbo",
            "name": "GPT-4 Turbo",
            "description": "Modelo avançado, ótima qualidade",
            "max_tokens": 4096,
        },
        {
            "id": "gpt-4",
            "name": "GPT-4",
            "description": "Modelo avançado e confiável",
            "max_tokens": 8192,
        },
        {
            "id": "gpt-4o-mini",
            "name": "GPT-4o Mini",
            "description": "Modelo rápido e econômico (bom para testes)",
            "max_tokens": 16384,
        },
    ]
