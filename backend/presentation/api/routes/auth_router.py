from fastapi import APIRouter, Depends, HTTPException, status

from application.dtos.auth_dtos import LoginInput, SignupInput
from application.use_cases.auth.login_use_case import LoginUseCase
from application.use_cases.auth.signup_use_case import SignupUseCase
from container import get_container
from domain.exceptions.domain_exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from presentation.api.schemas.auth_schemas import (
    TokenResponse,
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
)

router = APIRouter()


def _signup_use_case() -> SignupUseCase:
    return get_container().signup_use_case


def _login_use_case() -> LoginUseCase:
    return get_container().login_use_case


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    body: UserCreateRequest,
    use_case: SignupUseCase = Depends(_signup_use_case),
):
    try:
        result = await use_case.execute(
            SignupInput(
                email=body.email,
                username=body.username,
                password=body.password,
                full_name=body.full_name,
            )
        )
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return UserResponse(**result.__dict__)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: UserLoginRequest,
    use_case: LoginUseCase = Depends(_login_use_case),
):
    try:
        result = await use_case.execute(LoginInput(email=body.email, password=body.password))
    except (InvalidCredentialsError, InactiveUserError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(**result.__dict__)
