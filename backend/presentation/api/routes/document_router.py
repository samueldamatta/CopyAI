from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from typing import List, Optional

from application.use_cases.document.delete_document_use_case import DeleteDocumentUseCase
from application.use_cases.document.list_documents_use_case import ListDocumentsUseCase
from application.use_cases.document.upload_document_use_case import UploadDocumentUseCase
from container import get_container
from domain.entities.user import User
from domain.exceptions.domain_exceptions import DocumentNotFoundError
from presentation.dependencies import get_active_user

router = APIRouter()


def _upload_uc() -> UploadDocumentUseCase:
    return get_container().upload_document_use_case


def _list_uc() -> ListDocumentsUseCase:
    return get_container().list_documents_use_case


def _delete_uc() -> DeleteDocumentUseCase:
    return get_container().delete_document_use_case


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    conversation_id: Optional[str] = None,
    current_user: User = Depends(get_active_user),
    use_case: UploadDocumentUseCase = Depends(_upload_uc),
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas arquivos PDF são suportados",
        )
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo muito grande. Tamanho máximo: 10MB",
        )
    try:
        result = await use_case.execute(
            pdf_bytes=content,
            filename=file.filename,
            file_size=len(content),
            user_id=current_user.id,
            conversation_id=conversation_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar PDF: {e}",
        )
    return result


@router.get("/list")
async def list_documents(
    conversation_id: Optional[str] = None,
    current_user: User = Depends(get_active_user),
    use_case: ListDocumentsUseCase = Depends(_list_uc),
):
    return await use_case.execute(current_user.id, conversation_id)


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_active_user),
    use_case: DeleteDocumentUseCase = Depends(_delete_uc),
):
    try:
        await use_case.execute(document_id, current_user.id)
    except DocumentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {"message": "Documento e dados RAG excluídos com sucesso"}
