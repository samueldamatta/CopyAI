from fastapi import APIRouter, Depends

from middleware.auth import get_current_active_user
from models.user import UserModel
from schemas.auth import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_active_user)
):
    """Retorna as informações do usuário atual"""
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat()
    )

