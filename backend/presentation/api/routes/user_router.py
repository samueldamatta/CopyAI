from fastapi import APIRouter, Depends

from domain.entities.user import User
from presentation.api.schemas.auth_schemas import UserResponse
from presentation.dependencies import get_active_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_active_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat(),
    )
