from typing import Dict, List, Optional

from agents import Agent, Runner

from domain.gateways.ai_gateway import AIGateway
from ai.agents.agent_definitions import make_copywriter_agent, make_title_agent

_AVAILABLE_MODELS = [
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


class OpenAIAgentsGateway(AIGateway):
    def __init__(self):
        self._default_agent = make_copywriter_agent()
        self._title_agent = make_title_agent()

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
    ) -> str:
        try:
            agent = self._default_agent
            if model and model != "gpt-4o":
                agent = make_copywriter_agent(model=model)
            result = await Runner.run(agent, input=messages)
            return result.final_output
        except Exception as e:
            error = str(e).lower()
            if "authentication" in error or "api_key" in error:
                return "❌ Erro de autenticação com a API da OpenAI. Verifique sua chave de API no arquivo .env"
            if "quota" in error or "billing" in error:
                return "❌ Limite de uso da API OpenAI atingido. Verifique sua conta em https://platform.openai.com/account/billing"
            if "rate_limit" in error:
                return "⏳ Muitas requisições. Aguarde alguns segundos e tente novamente."
            return f"❌ Erro ao processar sua solicitação: {e}. Tente novamente."

    async def generate_title(self, first_message: str) -> str:
        try:
            result = await Runner.run(self._title_agent, first_message)
            title = result.final_output.strip().replace('"', "").replace("'", "")
            return title[:50]
        except Exception:
            return "Nova Conversa"

    def get_available_models(self) -> List[Dict[str, str]]:
        return _AVAILABLE_MODELS
