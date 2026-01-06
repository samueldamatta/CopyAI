from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Optional

from middleware.auth import get_current_active_user
from models.user import UserModel
from services.rag_service import rag_service
from database import get_database
from models.document import DocumentModel, DocumentChunk

router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    conversation_id: Optional[str] = None,
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Upload de PDF para RAG
    O PDF será processado, dividido em chunks e embeddings serão criados
    """
    # Validar tipo de arquivo
    if not file.content_type == "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas arquivos PDF são suportados"
        )
    
    # Validar tamanho (máximo 10MB)
    content = await file.read()
    file_size = len(content)
    if file_size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo muito grande. Tamanho máximo: 10MB"
        )
    
    try:
        # Processar PDF
        user_id = str(current_user.id)
        result = await rag_service.process_pdf_for_rag(
            pdf_file=content,
            filename=file.filename,
            user_id=user_id,
            conversation_id=conversation_id
        )
        
        # Salvar informações do documento no MongoDB
        db = get_database()
        document = DocumentModel(
            user_id=user_id,
            conversation_id=conversation_id,
            filename=file.filename,
            file_path=result["file_path"],
            file_size=file_size,
            collection_name=result["collection_name"],
            total_pages=result["total_pages"],
            chunks=[]  # Chunks ficam no ChromaDB (local)
        )
        
        document_dict = document.model_dump(by_alias=True, exclude={"id"})
        doc_result = await db.documents.insert_one(document_dict)
        
        return {
            **result,
            "document_id": str(doc_result.inserted_id),
            "status": "success"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar PDF: {str(e)}"
        )


@router.get("/list")
async def list_documents(
    conversation_id: Optional[str] = None,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Lista todos os documentos do usuário"""
    db = get_database()
    user_id = str(current_user.id)
    
    query = {"user_id": user_id}
    if conversation_id:
        query["conversation_id"] = conversation_id
    
    documents = []
    async for doc in db.documents.find(query).sort("created_at", -1):
        documents.append({
            "id": str(doc["_id"]),
            "filename": doc["filename"],
            "file_size": doc["file_size"],
            "total_pages": doc["total_pages"],
            "created_at": doc["created_at"].isoformat()
        })
    
    return documents


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Deleta um documento (arquivo físico, embeddings e registro no DB)"""
    db = get_database()
    user_id = str(current_user.id)
    
    from bson import ObjectId
    
    # Buscar documento para pegar file_path e collection_name
    document = await db.documents.find_one({
        "_id": ObjectId(document_id),
        "user_id": user_id
    })
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    # Deletar arquivo físico do disco
    if "file_path" in document:
        rag_service.delete_pdf_file(document["file_path"])
    
    # Deletar embeddings do ChromaDB
    if "collection_name" in document:
        rag_service.delete_collection(document["collection_name"])
    
    # Deletar registro do MongoDB
    await db.documents.delete_one({
        "_id": ObjectId(document_id),
        "user_id": user_id
    })
    
    return {"message": "Documento e dados RAG excluídos com sucesso"}

