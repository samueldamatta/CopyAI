from typing import List

from domain.repositories.conversation_repository import ConversationRepository
from application.dtos.conversation_dtos import ConversationListItem


class ListConversationsUseCase:
    def __init__(self, conversation_repo: ConversationRepository):
        self._repo = conversation_repo

    async def execute(self, user_id: str, include_archived: bool = False) -> List[ConversationListItem]:
        conversations = await self._repo.find_by_user(user_id, include_archived)
        return [
            ConversationListItem(
                id=conv.id,
                title=conv.title,
                copy_type=conv.copy_type,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
                message_count=len(conv.messages),
            )
            for conv in conversations
        ]
