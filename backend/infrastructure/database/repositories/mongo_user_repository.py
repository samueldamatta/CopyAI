from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class MongoUserRepository(UserRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._col = db.users

    async def find_by_email(self, email: str) -> Optional[User]:
        data = await self._col.find_one({"email": email})
        return self._to_entity(data) if data else None

    async def find_by_id(self, user_id: str) -> Optional[User]:
        data = await self._col.find_one({"_id": ObjectId(user_id)})
        return self._to_entity(data) if data else None

    async def find_by_username(self, username: str) -> Optional[User]:
        data = await self._col.find_one({"username": username})
        return self._to_entity(data) if data else None

    async def save(self, user: User) -> User:
        doc = {
            "email": user.email,
            "username": user.username,
            "hashed_password": user.hashed_password,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        result = await self._col.insert_one(doc)
        user.id = str(result.inserted_id)
        return user

    def _to_entity(self, data: dict) -> User:
        return User(
            id=str(data["_id"]),
            email=data["email"],
            username=data["username"],
            hashed_password=data["hashed_password"],
            full_name=data.get("full_name"),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
