from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from middleware.auth import get_current_active_user
from models.user import UserModel
from schemas.chat import ConversationResponse, ConversationList, ConversationCreate, ConversationUpdateBrief
from services.conversation_service import (
    create_conversation,
    get_conversation,
    get_user_conversations,
    delete_conversation,
    archive_conversation,
    update_conversation_brief
)

router = APIRouter()


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_new_conversation(
    conversation_data: ConversationCreate,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Cria uma nova conversa"""
    conversation = await create_conversation(
        user_id=str(current_user.id),
        title=conversation_data.title,
        copy_type=conversation_data.copy_type
    )
    
    return ConversationResponse(
        id=str(conversation.id),
        user_id=conversation.user_id,
        title=conversation.title,
        copy_type=conversation.copy_type,
        messages=[],
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        is_archived=conversation.is_archived
    )


@router.get("", response_model=List[ConversationList])
async def list_conversations(
    current_user: UserModel = Depends(get_current_active_user),
    include_archived: bool = False
):
    """Lista todas as conversas do usuário"""
    conversations = await get_user_conversations(
        user_id=str(current_user.id),
        include_archived=include_archived
    )
    
    return [
        ConversationList(
            id=str(conv.id),
            title=conv.title,
            copy_type=conv.copy_type,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=len(conv.messages)
        )
        for conv in conversations
    ]


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation_detail(
    conversation_id: str,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Obtém os detalhes de uma conversa específica"""
    conversation = await get_conversation(
        conversation_id=conversation_id,
        user_id=str(current_user.id)
    )
    
    # Serializar mensagens corretamente
    from schemas.chat import MessageResponse
    messages = [
        MessageResponse(
            role=msg.role,
            content=msg.content,
            timestamp=msg.timestamp
        )
        for msg in conversation.messages
    ]
    
    return ConversationResponse(
        id=str(conversation.id),
        user_id=conversation.user_id,
        title=conversation.title,
        copy_type=conversation.copy_type,
        messages=messages,
        brief=conversation.brief,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        is_archived=conversation.is_archived
    )


@router.patch("/{conversation_id}/brief", response_model=ConversationResponse)
async def update_brief(
    conversation_id: str,
    brief_data: ConversationUpdateBrief,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Atualiza o brief de uma conversa"""
    conversation = await update_conversation_brief(
        conversation_id=conversation_id,
        user_id=str(current_user.id),
        brief_data=brief_data.brief
    )
    
    # Mapear mensagens para resposta
    from schemas.chat import MessageResponse
    messages = [
        MessageResponse(
            role=msg.role,
            content=msg.content,
            timestamp=msg.timestamp
        )
        for msg in conversation.messages
    ]
    
    return ConversationResponse(
        id=str(conversation.id),
        user_id=conversation.user_id,
        title=conversation.title,
        copy_type=conversation.copy_type,
        messages=messages,
        brief=conversation.brief,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        is_archived=conversation.is_archived
    )


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation_endpoint(
    conversation_id: str,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Deleta uma conversa"""
    await delete_conversation(
        conversation_id=conversation_id,
        user_id=str(current_user.id)
    )


@router.post("/{conversation_id}/archive", status_code=status.HTTP_204_NO_CONTENT)
async def archive_conversation_endpoint(
    conversation_id: str,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Arquiva uma conversa"""
    await archive_conversation(
        conversation_id=conversation_id,
        user_id=str(current_user.id)
    )

