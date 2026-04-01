from domain.exceptions.domain_exceptions import DocumentNotFoundError
from domain.gateways.rag_gateway import RAGGateway
from domain.repositories.document_repository import DocumentRepository


class DeleteDocumentUseCase:
    def __init__(self, document_repo: DocumentRepository, rag_gateway: RAGGateway):
        self._document_repo = document_repo
        self._rag_gateway = rag_gateway

    async def execute(self, document_id: str, user_id: str) -> None:
        document = await self._document_repo.find_by_id(document_id, user_id)
        if not document:
            raise DocumentNotFoundError("Documento não encontrado")

        self._rag_gateway.delete_file(document.file_path)
        self._rag_gateway.delete_collection(document.collection_name)
        await self._document_repo.delete(document_id, user_id)
