from domain.entities.conversation import Conversation
from domain.repositories.conversation_repository import ConversationRepository
from application.dtos.conversation_dtos import CreateConversationInput, ConversationOutput


class CreateConversationUseCase:
    def __init__(self, conversation_repo: ConversationRepository):
        self._repo = conversation_repo

    async def execute(self, input: CreateConversationInput) -> ConversationOutput:
        conversation = await self._repo.save(
            Conversation(
                user_id=input.user_id,
                title=input.title or "Nova Conversa",
                copy_type=input.copy_type,
                brief=input.brief,
            )
        )
        return ConversationOutput(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            copy_type=conversation.copy_type,
            messages=[],
            brief=conversation.brief,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            is_archived=conversation.is_archived,
        )
