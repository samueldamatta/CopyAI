from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from models.user import PyObjectId


class DocumentChunk(BaseModel):
    """Chunk de documento para RAG"""
    content: str
    metadata: dict = {}
    embedding: Optional[List[float]] = None


class DocumentModel(BaseModel):
    """Modelo para documentos RAG (PDFs)"""
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "filename": "documento.pdf",
                "file_size": 1024000,
                "total_pages": 10
            }
        }
    )
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: str
    conversation_id: Optional[str] = None
    filename: str
    file_path: str  # Caminho do arquivo no disco local
    file_size: int
    mime_type: str = "application/pdf"
    collection_name: str  # Nome da coleção no ChromaDB
    chunks: List[DocumentChunk] = Field(default_factory=list)
    total_pages: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

