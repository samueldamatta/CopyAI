from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from application.dtos.conversation_dtos import CreateConversationInput
from application.use_cases.conversation.archive_conversation_use_case import ArchiveConversationUseCase
from application.use_cases.conversation.create_conversation_use_case import CreateConversationUseCase
from application.use_cases.conversation.delete_conversation_use_case import DeleteConversationUseCase
from application.use_cases.conversation.get_conversation_use_case import GetConversationUseCase
from application.use_cases.conversation.list_conversations_use_case import ListConversationsUseCase
from application.use_cases.conversation.update_brief_use_case import UpdateBriefUseCase
from container import get_container
from domain.entities.user import User
from domain.exceptions.domain_exceptions import ConversationNotFoundError
from presentation.api.schemas.chat_schemas import MessageResponse
from presentation.api.schemas.conversation_schemas import (
    ConversationCreateRequest,
    ConversationListResponse,
    ConversationResponse,
    ConversationUpdateBriefRequest,
)
from presentation.dependencies import get_active_user

router = APIRouter()


def _create_uc() -> CreateConversationUseCase:
    return get_container().create_conversation_use_case


def _list_uc() -> ListConversationsUseCase:
    return get_container().list_conversations_use_case


def _get_uc() -> GetConversationUseCase:
    return get_container().get_conversation_use_case


def _delete_uc() -> DeleteConversationUseCase:
    return get_container().delete_conversation_use_case


def _archive_uc() -> ArchiveConversationUseCase:
    return get_container().archive_conversation_use_case


def _brief_uc() -> UpdateBriefUseCase:
    return get_container().update_brief_use_case


def _conv_to_response(conv_out) -> ConversationResponse:
    return ConversationResponse(
        id=conv_out.id,
        user_id=conv_out.user_id,
        title=conv_out.title,
        copy_type=conv_out.copy_type,
        messages=[
            MessageResponse(role=m.role, content=m.content, timestamp=m.timestamp)
            for m in conv_out.messages
        ],
        brief=conv_out.brief,
        created_at=conv_out.created_at,
        updated_at=conv_out.updated_at,
        is_archived=conv_out.is_archived,
    )


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    body: ConversationCreateRequest,
    current_user: User = Depends(get_active_user),
    use_case: CreateConversationUseCase = Depends(_create_uc),
):
    result = await use_case.execute(
        CreateConversationInput(
            user_id=current_user.id,
            title=body.title,
            copy_type=body.copy_type or "geral",
        )
    )
    return _conv_to_response(result)


@router.get("", response_model=List[ConversationListResponse])
async def list_conversations(
    include_archived: bool = False,
    current_user: User = Depends(get_active_user),
    use_case: ListConversationsUseCase = Depends(_list_uc),
):
    items = await use_case.execute(current_user.id, include_archived)
    return [
        ConversationListResponse(
            id=item.id,
            title=item.title,
            copy_type=item.copy_type,
            created_at=item.created_at,
            updated_at=item.updated_at,
            message_count=item.message_count,
        )
        for item in items
    ]


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_active_user),
    use_case: GetConversationUseCase = Depends(_get_uc),
):
    try:
        result = await use_case.execute(conversation_id, current_user.id)
    except ConversationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return _conv_to_response(result)


@router.patch("/{conversation_id}/brief", response_model=ConversationResponse)
async def update_brief(
    conversation_id: str,
    body: ConversationUpdateBriefRequest,
    current_user: User = Depends(get_active_user),
    use_case: UpdateBriefUseCase = Depends(_brief_uc),
):
    try:
        result = await use_case.execute(conversation_id, current_user.id, body.brief)
    except ConversationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return _conv_to_response(result)


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_active_user),
    use_case: DeleteConversationUseCase = Depends(_delete_uc),
):
    try:
        await use_case.execute(conversation_id, current_user.id)
    except ConversationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{conversation_id}/archive", status_code=status.HTTP_204_NO_CONTENT)
async def archive_conversation(
    conversation_id: str,
    current_user: User = Depends(get_active_user),
    use_case: ArchiveConversationUseCase = Depends(_archive_uc),
):
    try:
        await use_case.execute(conversation_id, current_user.id)
    except ConversationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
