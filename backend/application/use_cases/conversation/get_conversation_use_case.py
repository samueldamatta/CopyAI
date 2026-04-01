from domain.exceptions.domain_exceptions import ConversationNotFoundError
from domain.repositories.conversation_repository import ConversationRepository
from application.dtos.chat_dtos import MessageOutput
from application.dtos.conversation_dtos import ConversationOutput


class GetConversationUseCase:
    def __init__(self, conversation_repo: ConversationRepository):
        self._repo = conversation_repo

    async def execute(self, conversation_id: str, user_id: str) -> ConversationOutput:
        conversation = await self._repo.find_by_id(conversation_id, user_id)
        if not conversation:
            raise ConversationNotFoundError("Conversa não encontrada")

        return ConversationOutput(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            copy_type=conversation.copy_type,
            messages=[
                MessageOutput(role=m.role, content=m.content, timestamp=m.timestamp)
                for m in conversation.messages
            ],
            brief=conversation.brief,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            is_archived=conversation.is_archived,
        )
