from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MessageRequest(BaseModel):
    content: str
    conversation_id: Optional[str] = None
    copy_type: Optional[str] = "geral"
    brief: Optional[dict] = None


class MessageResponse(BaseModel):
    role: str
    content: str
    timestamp: datetime


class ConversationCreate(BaseModel):
    title: Optional[str] = "Nova Conversa"
    copy_type: Optional[str] = "geral"


class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    copy_type: str
    messages: List[MessageResponse]
    brief: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    is_archived: bool

    class Config:
        from_attributes = True


class ConversationList(BaseModel):
    id: str
    title: str
    copy_type: str
    created_at: datetime
    updated_at: datetime
    message_count: int


class ConversationUpdateBrief(BaseModel):
    brief: dict

