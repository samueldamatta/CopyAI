from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Document:
    user_id: str
    filename: str
    file_path: str
    file_size: int
    collection_name: str
    total_pages: int = 0
    conversation_id: Optional[str] = None
    mime_type: str = "application/pdf"
    id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
