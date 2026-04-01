from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from container import init_container
from infrastructure.database.mongodb_client import connect, disconnect, get_database
from presentation.api.routes import (
    auth_router,
    chat_router,
    conversation_router,
    document_router,
    user_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect(settings.mongodb_url)
    db = get_database(settings.database_name)
    init_container(
        db=db,
        openai_api_key=settings.openai_api_key,
        jwt_settings={
            "secret_key": settings.secret_key,
            "algorithm": settings.algorithm,
            "expire_minutes": settings.access_token_expire_minutes,
        },
    )
    print(f"✅ Conectado ao MongoDB: {settings.database_name}")
    yield
    # Shutdown
    await disconnect()
    print("❌ Conexão com MongoDB fechada")


app = FastAPI(
    title="CopyAI API",
    description="API para agente de criação de copys com IA",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(user_router.router, prefix="/api/users", tags=["Usuários"])
app.include_router(conversation_router.router, prefix="/api/conversations", tags=["Conversas"])
app.include_router(chat_router.router, prefix="/api/chat", tags=["Chat"])
app.include_router(document_router.router, prefix="/api/documents", tags=["Documentos RAG"])


@app.get("/")
async def root():
    return {"message": "CopyAI API está rodando!", "version": "2.0.0", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
