from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.document import Document
from domain.repositories.document_repository import DocumentRepository


class MongoDocumentRepository(DocumentRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._col = db.documents

    async def find_by_id(self, document_id: str, user_id: str) -> Optional[Document]:
        data = await self._col.find_one(
            {"_id": ObjectId(document_id), "user_id": user_id}
        )
        return self._to_entity(data) if data else None

    async def find_by_user(self, user_id: str, conversation_id: Optional[str] = None) -> List[Document]:
        query = {"user_id": user_id}
        if conversation_id:
            query["conversation_id"] = conversation_id
        documents = []
        async for data in self._col.find(query).sort("created_at", -1):
            documents.append(self._to_entity(data))
        return documents

    async def save(self, document: Document) -> Document:
        doc = {
            "user_id": document.user_id,
            "conversation_id": document.conversation_id,
            "filename": document.filename,
            "file_path": document.file_path,
            "file_size": document.file_size,
            "mime_type": document.mime_type,
            "collection_name": document.collection_name,
            "chunks": [],
            "total_pages": document.total_pages,
            "created_at": document.created_at,
        }
        result = await self._col.insert_one(doc)
        document.id = str(result.inserted_id)
        return document

    async def delete(self, document_id: str, user_id: str) -> None:
        await self._col.delete_one(
            {"_id": ObjectId(document_id), "user_id": user_id}
        )

    def _to_entity(self, data: dict) -> Document:
        return Document(
            id=str(data["_id"]),
            user_id=data["user_id"],
            conversation_id=data.get("conversation_id"),
            filename=data["filename"],
            file_path=data["file_path"],
            file_size=data["file_size"],
            mime_type=data.get("mime_type", "application/pdf"),
            collection_name=data["collection_name"],
            total_pages=data.get("total_pages", 0),
            created_at=data.get("created_at"),
        )
