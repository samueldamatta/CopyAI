from domain.entities.conversation import Conversation, Message
from domain.exceptions.domain_exceptions import ConversationNotFoundError
from domain.gateways.ai_gateway import AIGateway
from domain.gateways.rag_gateway import RAGGateway
from domain.repositories.conversation_repository import ConversationRepository
from application.dtos.chat_dtos import SendMessageInput, MessageOutput


class SendMessageUseCase:
    def __init__(
        self,
        conversation_repo: ConversationRepository,
        ai_gateway: AIGateway,
        rag_gateway: RAGGateway,
    ):
        self._conversation_repo = conversation_repo
        self._ai_gateway = ai_gateway
        self._rag_gateway = rag_gateway

    async def execute(self, input: SendMessageInput) -> MessageOutput:
        user_id = input.user_id

        if not input.conversation_id:
            conversation = await self._conversation_repo.save(
                Conversation(
                    user_id=user_id,
                    copy_type=input.copy_type or "geral",
                    brief=input.brief,
                )
            )
            is_first = True
        else:
            conversation = await self._conversation_repo.find_by_id(
                input.conversation_id, user_id
            )
            if not conversation:
                raise ConversationNotFoundError("Conversa não encontrada")
            if input.brief:
                await self._conversation_repo.update_brief(
                    input.conversation_id, user_id, input.brief
                )
            is_first = len(conversation.messages) == 0

        conversation_id = conversation.id

        # Save user message
        user_msg = Message(role="user", content=input.content)
        conversation = await self._conversation_repo.add_message(
            conversation_id, user_id, user_msg
        )

        # Generate title on first message (fire-and-forget, don't block)
        if is_first:
            title = await self._ai_gateway.generate_title(input.content)
            await self._conversation_repo.update_title(conversation_id, user_id, title)

        # Build message history for AI
        messages = [
            {"role": m.role, "content": m.content} for m in conversation.messages
        ]

        # Inject RAG context if available
        try:
            collection = f"user_{user_id}_{conversation_id}"
            context = await self._rag_gateway.search_similar(input.content, collection)
            if context:
                messages.insert(
                    0,
                    {
                        "role": "system",
                        "content": f"Use o seguinte contexto dos documentos para responder:\n\n{context}",
                    },
                )
        except Exception:
            pass

        # Generate AI response
        ai_content = await self._ai_gateway.generate_response(messages)

        # Save assistant message
        ai_msg = Message(role="assistant", content=ai_content)
        conversation = await self._conversation_repo.add_message(
            conversation_id, user_id, ai_msg
        )

        last_msg = conversation.messages[-1]
        return MessageOutput(
            role=last_msg.role,
            content=last_msg.content,
            timestamp=last_msg.timestamp,
        )
