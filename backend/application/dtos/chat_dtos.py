from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SendMessageInput:
    content: str
    user_id: str
    conversation_id: Optional[str] = None
    copy_type: str = "geral"
    brief: Optional[dict] = None


@dataclass
class MessageOutput:
    role: str
    content: str
    timestamp: datetime
