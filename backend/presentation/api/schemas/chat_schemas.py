from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SendMessageRequest(BaseModel):
    content: str
    conversation_id: Optional[str] = None
    copy_type: Optional[str] = "geral"
    brief: Optional[dict] = None


class MessageResponse(BaseModel):
    role: str
    content: str
    timestamp: datetime
