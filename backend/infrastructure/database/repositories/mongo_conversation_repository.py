from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.conversation import Conversation, Message
from domain.repositories.conversation_repository import ConversationRepository


class MongoConversationRepository(ConversationRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._col = db.conversations

    async def find_by_id(self, conversation_id: str, user_id: str) -> Optional[Conversation]:
        data = await self._col.find_one(
            {"_id": ObjectId(conversation_id), "user_id": user_id}
        )
        return self._to_entity(data) if data else None

    async def find_by_user(self, user_id: str, include_archived: bool = False) -> List[Conversation]:
        query = {"user_id": user_id}
        if not include_archived:
            query["is_archived"] = False
        conversations = []
        async for data in self._col.find(query).sort("updated_at", -1):
            conversations.append(self._to_entity(data))
        return conversations

    async def save(self, conversation: Conversation) -> Conversation:
        doc = {
            "user_id": conversation.user_id,
            "title": conversation.title,
            "copy_type": conversation.copy_type,
            "messages": [],
            "brief": conversation.brief,
            "is_archived": conversation.is_archived,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
        }
        result = await self._col.insert_one(doc)
        conversation.id = str(result.inserted_id)
        return conversation

    async def add_message(self, conversation_id: str, user_id: str, message: Message) -> Conversation:
        msg_doc = {"role": message.role, "content": message.content, "timestamp": message.timestamp}
        data = await self._col.find_one_and_update(
            {"_id": ObjectId(conversation_id), "user_id": user_id},
            {"$push": {"messages": msg_doc}, "$set": {"updated_at": datetime.utcnow()}},
            return_document=True,
        )
        return self._to_entity(data)

    async def update_title(self, conversation_id: str, user_id: str, title: str) -> None:
        await self._col.update_one(
            {"_id": ObjectId(conversation_id), "user_id": user_id},
            {"$set": {"title": title, "updated_at": datetime.utcnow()}},
        )

    async def update_brief(self, conversation_id: str, user_id: str, brief: dict) -> Conversation:
        data = await self._col.find_one_and_update(
            {"_id": ObjectId(conversation_id), "user_id": user_id},
            {"$set": {"brief": brief, "updated_at": datetime.utcnow()}},
            return_document=True,
        )
        return self._to_entity(data)

    async def delete(self, conversation_id: str, user_id: str) -> None:
        await self._col.delete_one(
            {"_id": ObjectId(conversation_id), "user_id": user_id}
        )

    async def archive(self, conversation_id: str, user_id: str) -> None:
        await self._col.update_one(
            {"_id": ObjectId(conversation_id), "user_id": user_id},
            {"$set": {"is_archived": True, "updated_at": datetime.utcnow()}},
        )

    def _to_entity(self, data: dict) -> Conversation:
        return Conversation(
            id=str(data["_id"]),
            user_id=data["user_id"],
            title=data.get("title", "Nova Conversa"),
            copy_type=data.get("copy_type", "geral"),
            messages=[
                Message(
                    role=m["role"],
                    content=m["content"],
                    timestamp=m.get("timestamp", datetime.utcnow()),
                )
                for m in data.get("messages", [])
            ],
            brief=data.get("brief"),
            is_archived=data.get("is_archived", False),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
