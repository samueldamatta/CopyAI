from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from typing import Dict, List

from middleware.auth import get_current_active_user
from models.user import UserModel
from schemas.chat import MessageRequest, MessageResponse
from services.conversation_service import (
    create_conversation,
    get_conversation,
    add_message_to_conversation,
    update_conversation_title,
    update_conversation_brief
)
from services.ai_service import generate_copy_response, get_available_models
from services.rag_service import rag_service

router = APIRouter()


@router.get("/models")
async def list_available_models(
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Lista os modelos ChatGPT disponíveis para uso
    """
    return {
        "models": get_available_models(),
        "default": "gpt-4-turbo-preview",
        "info": "Use o campo 'id' para especificar o modelo nas requisições"
    }


@router.post("/message", response_model=MessageResponse)
async def send_message(
    message_data: MessageRequest,
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Envia uma mensagem e recebe resposta do agente de IA
    """
    user_id = str(current_user.id)
    
    # Se não houver conversation_id, cria uma nova conversa
    if not message_data.conversation_id:
        conversation = await create_conversation(
            user_id=user_id,
            copy_type=message_data.copy_type,
            brief=message_data.brief
        )
        conversation_id = str(conversation.id)
        is_first_message = True
    else:
        conversation_id = message_data.conversation_id
        # Atualiza o brief se enviado em uma conversa existente
        if message_data.brief:
            await update_conversation_brief(conversation_id, user_id, message_data.brief)
            
        conversation = await get_conversation(conversation_id, user_id)
        is_first_message = len(conversation.messages) == 0
    
    # Adiciona a mensagem do usuário
    await add_message_to_conversation(
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=message_data.content
    )
    
    # Se for a primeira mensagem, atualiza o título
    if is_first_message:
        await update_conversation_title(
            conversation_id=conversation_id,
            user_id=user_id,
            first_message=message_data.content
        )
    
    # Busca a conversa atualizada para pegar o histórico
    conversation = await get_conversation(conversation_id, user_id)
    
    # Prepara o histórico de mensagens para a IA
    messages_for_ai = [
        {"role": msg.role, "content": msg.content}
        for msg in conversation.messages
    ]
    
    # **RAG: Busca contexto relevante em documentos (se houver)**
    try:
        collection_name = f"user_{user_id}_{conversation_id}"
        relevant_docs = await rag_service.similarity_search(
            query=message_data.content,
            collection_name=collection_name,
            k=3  # Top 3 chunks mais relevantes
        )
        
        # Se encontrou contexto relevante, adiciona nas mensagens
        if relevant_docs:
            context = rag_service.format_context_for_llm(relevant_docs)
            # Adiciona contexto como mensagem do sistema
            messages_for_ai.insert(0, {
                "role": "system",
                "content": f"Use o seguinte contexto dos documentos para responder:\n\n{context}"
            })
    except Exception as e:
        print(f"⚠️ Erro ao buscar contexto RAG: {e}")
        # Continua sem RAG se houver erro
    
    # Gera resposta da IA (agora com contexto RAG se disponível)
    ai_response = await generate_copy_response(messages_for_ai)
    
    # Adiciona a resposta da IA na conversa
    conversation = await add_message_to_conversation(
        conversation_id=conversation_id,
        user_id=user_id,
        role="assistant",
        content=ai_response
    )
    
    # Retorna a última mensagem (resposta da IA)
    last_message = conversation.messages[-1]
    return MessageResponse(
        role=last_message.role,
        content=last_message.content,
        timestamp=last_message.timestamp
    )


# Armazena conexões WebSocket ativas
active_connections: Dict[str, WebSocket] = {}


@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    """
    WebSocket para chat em tempo real
    Nota: Para autenticação via WebSocket, você precisaria passar o token
    como query parameter ou no primeiro payload
    """
    await websocket.accept()
    
    try:
        # Armazena a conexão
        active_connections[conversation_id] = websocket
        
        while True:
            # Recebe mensagem do cliente
            data = await websocket.receive_json()
            
            user_message = data.get("content")
            user_id = data.get("user_id")  # Em produção, extrair do token JWT
            
            if not user_message or not user_id:
                await websocket.send_json({
                    "error": "Mensagem ou user_id não fornecido"
                })
                continue
            
            # Adiciona mensagem do usuário
            await add_message_to_conversation(
                conversation_id=conversation_id,
                user_id=user_id,
                role="user",
                content=user_message
            )
            
            # Busca histórico
            conversation = await get_conversation(conversation_id, user_id)
            messages_for_ai = [
                {"role": msg.role, "content": msg.content}
                for msg in conversation.messages
            ]
            
            # Gera resposta
            ai_response = await generate_copy_response(messages_for_ai)
            
            # Salva resposta
            await add_message_to_conversation(
                conversation_id=conversation_id,
                user_id=user_id,
                role="assistant",
                content=ai_response
            )
            
            # Envia resposta ao cliente
            await websocket.send_json({
                "role": "assistant",
                "content": ai_response,
                "conversation_id": conversation_id
            })
    
    except WebSocketDisconnect:
        if conversation_id in active_connections:
            del active_connections[conversation_id]
    except Exception as e:
        print(f"Erro no WebSocket: {e}")
        if conversation_id in active_connections:
            del active_connections[conversation_id]

