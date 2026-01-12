from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from models.user import PyObjectId


class Message(BaseModel):
    role: str  # "user" ou "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "title": "Copy para produto X",
                "messages": [
                    {
                        "role": "user",
                        "content": "Crie uma copy para produto X"
                    }
                ]
            }
        }
    )
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: str
    title: str = "Nova Conversa"
    copy_type: str = "geral"  # Tipo de copy: geral, anuncios, redes-sociais, etc.
    messages: List[Message] = Field(default_factory=list)
    brief: Optional[dict] = None  # Dados do brief (público, dor, oferta, etc.)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_archived: bool = False

