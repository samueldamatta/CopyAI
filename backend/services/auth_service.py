from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from bson import ObjectId
import hashlib

from config import settings
from database import get_database
from models.user import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prepare_password(password: str) -> str:
    """
    Prepara a senha para o bcrypt usando SHA256 se necessário.
    Isso permite senhas de qualquer tamanho contornando a limitação de 72 bytes do bcrypt.
    """
    password_bytes = password.encode('utf-8')
    
    # Se a senha é maior que 72 bytes, usa SHA256 primeiro e retorna como string hex
    if len(password_bytes) > 72:
        return hashlib.sha256(password_bytes).hexdigest()
    
    return password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    prepared_password = _prepare_password(plain_password)
    return pwd_context.verify(prepared_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera o hash da senha"""
    prepared_password = _prepare_password(password)
    return pwd_context.hash(prepared_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def authenticate_user(email: str, password: str) -> Optional[UserModel]:
    """Autentica um usuário"""
    db = get_database()
    user_data = await db.users.find_one({"email": email})
    
    if not user_data:
        return None
    
    user = UserModel(**user_data)
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


async def get_user_by_email(email: str) -> Optional[UserModel]:
    """Busca um usuário pelo email"""
    db = get_database()
    user_data = await db.users.find_one({"email": email})
    
    if user_data:
        return UserModel(**user_data)
    return None


async def get_user_by_id(user_id: str) -> Optional[UserModel]:
    """Busca um usuário pelo ID"""
    db = get_database()
    user_data = await db.users.find_one({"_id": ObjectId(user_id)})
    
    if user_data:
        return UserModel(**user_data)
    return None


async def create_user(email: str, username: str, password: str, full_name: Optional[str] = None) -> UserModel:
    """Cria um novo usuário"""
    db = get_database()
    
    # Verifica se o email já existe
    existing_user = await db.users.find_one({"email": email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Verifica se o username já existe
    existing_username = await db.users.find_one({"username": username})
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já cadastrado"
        )
    
    # Cria o usuário
    user = UserModel(
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        full_name=full_name
    )
    
    user_dict = user.model_dump(by_alias=True, exclude={"id"})
    result = await db.users.insert_one(user_dict)
    user.id = result.inserted_id
    
    return user

