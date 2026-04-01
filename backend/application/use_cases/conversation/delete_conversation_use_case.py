from domain.exceptions.domain_exceptions import ConversationNotFoundError
from domain.repositories.conversation_repository import ConversationRepository


class DeleteConversationUseCase:
    def __init__(self, conversation_repo: ConversationRepository):
        self._repo = conversation_repo

    async def execute(self, conversation_id: str, user_id: str) -> None:
        conversation = await self._repo.find_by_id(conversation_id, user_id)
        if not conversation:
            raise ConversationNotFoundError("Conversa não encontrada")
        await self._repo.delete(conversation_id, user_id)
