from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.document import Document


class DocumentRepository(ABC):
    @abstractmethod
    async def find_by_id(self, document_id: str, user_id: str) -> Optional[Document]: ...

    @abstractmethod
    async def find_by_user(self, user_id: str, conversation_id: Optional[str] = None) -> List[Document]: ...

    @abstractmethod
    async def save(self, document: Document) -> Document: ...

    @abstractmethod
    async def delete(self, document_id: str, user_id: str) -> None: ...
