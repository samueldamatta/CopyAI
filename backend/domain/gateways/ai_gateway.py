from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class AIGateway(ABC):
    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
    ) -> str: ...

    @abstractmethod
    async def generate_title(self, first_message: str) -> str: ...

    @abstractmethod
    def get_available_models(self) -> List[Dict[str, str]]: ...
