from typing import Optional

from domain.entities.document import Document
from domain.gateways.rag_gateway import RAGGateway
from domain.repositories.document_repository import DocumentRepository
from application.dtos.conversation_dtos import DocumentOutput


class UploadDocumentUseCase:
    def __init__(self, document_repo: DocumentRepository, rag_gateway: RAGGateway):
        self._document_repo = document_repo
        self._rag_gateway = rag_gateway

    async def execute(
        self,
        pdf_bytes: bytes,
        filename: str,
        file_size: int,
        user_id: str,
        conversation_id: Optional[str] = None,
    ) -> dict:
        result = await self._rag_gateway.process_pdf(
            pdf_bytes=pdf_bytes,
            filename=filename,
            user_id=user_id,
            conversation_id=conversation_id,
        )

        document = Document(
            user_id=user_id,
            conversation_id=conversation_id,
            filename=filename,
            file_path=result["file_path"],
            file_size=file_size,
            collection_name=result["collection_name"],
            total_pages=result["total_pages"],
        )
        document = await self._document_repo.save(document)

        return {**result, "document_id": document.id, "status": "success"}
