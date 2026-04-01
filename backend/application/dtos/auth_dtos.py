from dataclasses import dataclass
from typing import Optional


@dataclass
class SignupInput:
    email: str
    username: str
    password: str
    full_name: Optional[str] = None


@dataclass
class LoginInput:
    email: str
    password: str


@dataclass
class AuthOutput:
    access_token: str
    token_type: str = "bearer"


@dataclass
class UserOutput:
    id: str
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: str
