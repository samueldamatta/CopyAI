from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]: ...

    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]: ...

    @abstractmethod
    async def save(self, user: User) -> User: ...
