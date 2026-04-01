from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from presentation.api.schemas.chat_schemas import MessageResponse


class ConversationCreateRequest(BaseModel):
    title: Optional[str] = "Nova Conversa"
    copy_type: Optional[str] = "geral"


class ConversationUpdateBriefRequest(BaseModel):
    brief: dict


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


class ConversationListResponse(BaseModel):
    id: str
    title: str
    copy_type: str
    created_at: datetime
    updated_at: datetime
    message_count: int
