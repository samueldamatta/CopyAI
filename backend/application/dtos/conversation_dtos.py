from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from application.dtos.chat_dtos import MessageOutput


@dataclass
class CreateConversationInput:
    user_id: str
    title: Optional[str] = None
    copy_type: str = "geral"
    brief: Optional[dict] = None


@dataclass
class ConversationOutput:
    id: str
    user_id: str
    title: str
    copy_type: str
    messages: List[MessageOutput]
    created_at: datetime
    updated_at: datetime
    is_archived: bool
    brief: Optional[dict] = None


@dataclass
class ConversationListItem:
    id: str
    title: str
    copy_type: str
    created_at: datetime
    updated_at: datetime
    message_count: int


@dataclass
class DocumentOutput:
    id: str
    filename: str
    file_size: int
    total_pages: int
    created_at: str
