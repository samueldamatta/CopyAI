from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from typing import Dict

from application.dtos.chat_dtos import SendMessageInput
from application.use_cases.chat.send_message_use_case import SendMessageUseCase
from container import get_container
from domain.entities.user import User
from domain.exceptions.domain_exceptions import ConversationNotFoundError
from presentation.api.schemas.chat_schemas import MessageResponse, SendMessageRequest
from presentation.dependencies import get_active_user

router = APIRouter()

_active_ws: Dict[str, WebSocket] = {}


def _send_message_use_case() -> SendMessageUseCase:
    return get_container().send_message_use_case


@router.get("/models")
async def list_models(current_user: User = Depends(get_active_user)):
    return {
        "models": get_container().ai_gateway.get_available_models(),
        "default": "gpt-4o",
        "info": "Use o campo 'id' para especificar o modelo nas requisições",
    }


@router.post("/message", response_model=MessageResponse)
async def send_message(
    body: SendMessageRequest,
    current_user: User = Depends(get_active_user),
    use_case: SendMessageUseCase = Depends(_send_message_use_case),
):
    try:
        result = await use_case.execute(
            SendMessageInput(
                content=body.content,
                user_id=current_user.id,
                conversation_id=body.conversation_id,
                copy_type=body.copy_type or "geral",
                brief=body.brief,
            )
        )
    except ConversationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return MessageResponse(role=result.role, content=result.content, timestamp=result.timestamp)


@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    await websocket.accept()
    try:
        _active_ws[conversation_id] = websocket
        while True:
            await websocket.receive_json()
            await websocket.send_json({"error": "WebSocket autenticado ainda não implementado"})
    except WebSocketDisconnect:
        _active_ws.pop(conversation_id, None)
    except Exception as e:
        print(f"WebSocket error: {e}")
        _active_ws.pop(conversation_id, None)
