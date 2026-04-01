from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    email: str
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
