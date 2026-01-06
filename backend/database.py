from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from config import settings

client: Optional[AsyncIOMotorClient] = None


async def connect_to_mongo():
    """Conecta ao MongoDB"""
    global client
    client = AsyncIOMotorClient(settings.mongodb_url)
    print(f"✅ Conectado ao MongoDB: {settings.database_name}")


async def close_mongo_connection():
    """Fecha a conexão com o MongoDB"""
    global client
    if client:
        client.close()
        print("❌ Conexão com MongoDB fechada")


def get_database():
    """Retorna a instância do banco de dados"""
    return client[settings.database_name]

