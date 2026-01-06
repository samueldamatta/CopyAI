from fastapi import APIRouter, HTTPException, status
from datetime import timedelta

from config import settings
from schemas.auth import UserCreate, UserLogin, Token, UserResponse
from services.auth_service import (
    authenticate_user,
    create_access_token,
    create_user
)

router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):
    """Registra um novo usuário"""
    user = await create_user(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        full_name=user_data.full_name
    )
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at.isoformat()
    )


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """Autentica um usuário e retorna um token JWT"""
    user = await authenticate_user(user_data.email, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

