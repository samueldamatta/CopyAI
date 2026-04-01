from abc import ABC, abstractmethod
from typing import Optional


class RAGGateway(ABC):
    @abstractmethod
    async def process_pdf(
        self,
        pdf_bytes: bytes,
        filename: str,
        user_id: str,
        conversation_id: Optional[str] = None,
    ) -> dict: ...

    @abstractmethod
    async def search_similar(
        self,
        query: str,
        collection_name: str,
        k: int = 3,
    ) -> str: ...

    @abstractmethod
    def delete_collection(self, collection_name: str) -> None: ...

    @abstractmethod
    def delete_file(self, file_path: str) -> None: ...
