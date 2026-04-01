from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.conversation import Conversation, Message


class ConversationRepository(ABC):
    @abstractmethod
    async def find_by_id(self, conversation_id: str, user_id: str) -> Optional[Conversation]: ...

    @abstractmethod
    async def find_by_user(self, user_id: str, include_archived: bool = False) -> List[Conversation]: ...

    @abstractmethod
    async def save(self, conversation: Conversation) -> Conversation: ...

    @abstractmethod
    async def add_message(self, conversation_id: str, user_id: str, message: Message) -> Conversation: ...

    @abstractmethod
    async def update_title(self, conversation_id: str, user_id: str, title: str) -> None: ...

    @abstractmethod
    async def update_brief(self, conversation_id: str, user_id: str, brief: dict) -> Conversation: ...

    @abstractmethod
    async def delete(self, conversation_id: str, user_id: str) -> None: ...

    @abstractmethod
    async def archive(self, conversation_id: str, user_id: str) -> None: ...
