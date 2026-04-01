from typing import List, Optional

from domain.repositories.document_repository import DocumentRepository
from application.dtos.conversation_dtos import DocumentOutput


class ListDocumentsUseCase:
    def __init__(self, document_repo: DocumentRepository):
        self._repo = document_repo

    async def execute(self, user_id: str, conversation_id: Optional[str] = None) -> List[DocumentOutput]:
        documents = await self._repo.find_by_user(user_id, conversation_id)
        return [
            DocumentOutput(
                id=doc.id,
                filename=doc.filename,
                file_size=doc.file_size,
                total_pages=doc.total_pages,
                created_at=doc.created_at.isoformat(),
            )
            for doc in documents
        ]
