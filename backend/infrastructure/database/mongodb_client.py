from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

_client: Optional[AsyncIOMotorClient] = None


async def connect(mongodb_url: str) -> AsyncIOMotorClient:
    global _client
    _client = AsyncIOMotorClient(mongodb_url)
    return _client


async def disconnect() -> None:
    global _client
    if _client:
        _client.close()
        _client = None


def get_client() -> AsyncIOMotorClient:
    if _client is None:
        raise RuntimeError("MongoDB client not initialized. Call connect() first.")
    return _client


def get_database(db_name: str) -> AsyncIOMotorDatabase:
    return get_client()[db_name]
