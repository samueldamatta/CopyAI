from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status

from database import get_database
from models.conversation import ConversationModel, Message
from services.ai_service import generate_conversation_title


async def create_conversation(user_id: str, title: Optional[str] = None, copy_type: Optional[str] = "geral") -> ConversationModel:
    """Cria uma nova conversa"""
    db = get_database()
    
    conversation = ConversationModel(
        user_id=user_id,
        title=title or "Nova Conversa",
        copy_type=copy_type or "geral"
    )
    
    conversation_dict = conversation.model_dump(by_alias=True, exclude={"id"})
    result = await db.conversations.insert_one(conversation_dict)
    conversation.id = result.inserted_id
    
    return conversation


async def get_conversation(conversation_id: str, user_id: str) -> ConversationModel:
    """Busca uma conversa pelo ID"""
    db = get_database()
    
    conversation_data = await db.conversations.find_one({
        "_id": ObjectId(conversation_id),
        "user_id": user_id
    })
    
    if not conversation_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversa não encontrada"
        )
    
    return ConversationModel(**conversation_data)


async def get_user_conversations(user_id: str, include_archived: bool = False) -> List[ConversationModel]:
    """Busca todas as conversas de um usuário"""
    db = get_database()
    
    query = {"user_id": user_id}
    if not include_archived:
        query["is_archived"] = False
    
    conversations = []
    async for conversation_data in db.conversations.find(query).sort("updated_at", -1):
        conversations.append(ConversationModel(**conversation_data))
    
    return conversations


async def add_message_to_conversation(
    conversation_id: str,
    user_id: str,
    role: str,
    content: str
) -> ConversationModel:
    """Adiciona uma mensagem a uma conversa"""
    db = get_database()
    
    message = Message(role=role, content=content)
    
    result = await db.conversations.find_one_and_update(
        {
            "_id": ObjectId(conversation_id),
            "user_id": user_id
        },
        {
            "$push": {"messages": message.model_dump()},
            "$set": {"updated_at": datetime.utcnow()}
        },
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversa não encontrada"
        )
    
    return ConversationModel(**result)


async def update_conversation_title(conversation_id: str, user_id: str, first_message: str):
    """Atualiza o título da conversa baseado na primeira mensagem"""
    db = get_database()
    
    # Gera título usando IA
    title = await generate_conversation_title(first_message)
    
    await db.conversations.update_one(
        {
            "_id": ObjectId(conversation_id),
            "user_id": user_id
        },
        {
            "$set": {
                "title": title,
                "updated_at": datetime.utcnow()
            }
        }
    )


async def delete_conversation(conversation_id: str, user_id: str):
    """Deleta uma conversa"""
    db = get_database()
    
    result = await db.conversations.delete_one({
        "_id": ObjectId(conversation_id),
        "user_id": user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversa não encontrada"
        )


async def archive_conversation(conversation_id: str, user_id: str):
    """Arquiva uma conversa"""
    db = get_database()
    
    result = await db.conversations.update_one(
        {
            "_id": ObjectId(conversation_id),
            "user_id": user_id
        },
        {
            "$set": {
                "is_archived": True,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversa não encontrada"
        )

