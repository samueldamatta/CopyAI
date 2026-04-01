from domain.exceptions.domain_exceptions import InvalidCredentialsError, InactiveUserError
from domain.repositories.user_repository import UserRepository
from application.dtos.auth_dtos import LoginInput, AuthOutput


class LoginUseCase:
    def __init__(self, user_repo: UserRepository, password_service, token_service):
        self._user_repo = user_repo
        self._password_service = password_service
        self._token_service = token_service

    async def execute(self, input: LoginInput) -> AuthOutput:
        user = await self._user_repo.find_by_email(input.email)

        if not user or not self._password_service.verify(input.password, user.hashed_password):
            raise InvalidCredentialsError("Email ou senha incorretos")

        if not user.is_active:
            raise InactiveUserError("Usuário inativo")

        token = self._token_service.create_access_token({"sub": user.email})
        return AuthOutput(access_token=token)
