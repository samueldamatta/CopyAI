"""
Dependency Injection Container.

This is the only module that knows about all layers simultaneously.
It wires infrastructure implementations to domain interfaces,
and builds application use-case instances.
"""
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorDatabase

from application.use_cases.auth.login_use_case import LoginUseCase
from application.use_cases.auth.signup_use_case import SignupUseCase
from application.use_cases.chat.send_message_use_case import SendMessageUseCase
from application.use_cases.conversation.archive_conversation_use_case import ArchiveConversationUseCase
from application.use_cases.conversation.create_conversation_use_case import CreateConversationUseCase
from application.use_cases.conversation.delete_conversation_use_case import DeleteConversationUseCase
from application.use_cases.conversation.get_conversation_use_case import GetConversationUseCase
from application.use_cases.conversation.list_conversations_use_case import ListConversationsUseCase
from application.use_cases.conversation.update_brief_use_case import UpdateBriefUseCase
from application.use_cases.document.delete_document_use_case import DeleteDocumentUseCase
from application.use_cases.document.list_documents_use_case import ListDocumentsUseCase
from application.use_cases.document.upload_document_use_case import UploadDocumentUseCase
from ai.workers.openai_agents_gateway import OpenAIAgentsGateway
from infrastructure.auth.jwt_token_service import JWTTokenService
from infrastructure.auth.password_service import PasswordService
from infrastructure.database.repositories.mongo_conversation_repository import MongoConversationRepository
from infrastructure.database.repositories.mongo_document_repository import MongoDocumentRepository
from infrastructure.database.repositories.mongo_user_repository import MongoUserRepository
from infrastructure.rag.chromadb_rag_gateway import ChromaDBRAGGateway


class Container:
    """Holds all wired-up dependencies for the application."""

    def __init__(self, db: AsyncIOMotorDatabase, openai_api_key: str, jwt_settings: dict):
        # --- Infrastructure ---
        self.password_service = PasswordService()
        self.token_service = JWTTokenService(**jwt_settings)

        storage_dir = str(Path(__file__).parent / "storage")
        self.rag_gateway = ChromaDBRAGGateway(
            openai_api_key=openai_api_key,
            base_storage_dir=storage_dir,
        )
        self.ai_gateway = OpenAIAgentsGateway()

        # --- Repositories ---
        self.user_repo = MongoUserRepository(db)
        self.conversation_repo = MongoConversationRepository(db)
        self.document_repo = MongoDocumentRepository(db)

        # --- Use Cases: Auth ---
        self.signup_use_case = SignupUseCase(self.user_repo, self.password_service)
        self.login_use_case = LoginUseCase(self.user_repo, self.password_service, self.token_service)

        # --- Use Cases: Chat ---
        self.send_message_use_case = SendMessageUseCase(
            self.conversation_repo, self.ai_gateway, self.rag_gateway
        )

        # --- Use Cases: Conversation ---
        self.create_conversation_use_case = CreateConversationUseCase(self.conversation_repo)
        self.list_conversations_use_case = ListConversationsUseCase(self.conversation_repo)
        self.get_conversation_use_case = GetConversationUseCase(self.conversation_repo)
        self.delete_conversation_use_case = DeleteConversationUseCase(self.conversation_repo)
        self.archive_conversation_use_case = ArchiveConversationUseCase(self.conversation_repo)
        self.update_brief_use_case = UpdateBriefUseCase(self.conversation_repo)

        # --- Use Cases: Document ---
        self.upload_document_use_case = UploadDocumentUseCase(self.document_repo, self.rag_gateway)
        self.list_documents_use_case = ListDocumentsUseCase(self.document_repo)
        self.delete_document_use_case = DeleteDocumentUseCase(self.document_repo, self.rag_gateway)


# Single global container instance, set during app startup
_container: Container = None


def init_container(db: AsyncIOMotorDatabase, openai_api_key: str, jwt_settings: dict) -> Container:
    global _container
    _container = Container(db=db, openai_api_key=openai_api_key, jwt_settings=jwt_settings)
    return _container


def get_container() -> Container:
    if _container is None:
        raise RuntimeError("Container not initialized. Call init_container() during app startup.")
    return _container
