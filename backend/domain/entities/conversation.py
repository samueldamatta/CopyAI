from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Message:
    role: str  # "user" | "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Conversation:
    user_id: str
    title: str = "Nova Conversa"
    copy_type: str = "geral"
    messages: List[Message] = field(default_factory=list)
    brief: Optional[dict] = None
    is_archived: bool = False
    id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
