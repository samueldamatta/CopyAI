from domain.entities.user import User
from domain.exceptions.domain_exceptions import UserAlreadyExistsError
from domain.repositories.user_repository import UserRepository
from application.dtos.auth_dtos import SignupInput, UserOutput


class SignupUseCase:
    def __init__(self, user_repo: UserRepository, password_service):
        self._user_repo = user_repo
        self._password_service = password_service

    async def execute(self, input: SignupInput) -> UserOutput:
        if await self._user_repo.find_by_email(input.email):
            raise UserAlreadyExistsError("Email já cadastrado")

        if await self._user_repo.find_by_username(input.username):
            raise UserAlreadyExistsError("Nome de usuário já cadastrado")

        user = User(
            email=input.email,
            username=input.username,
            hashed_password=self._password_service.hash(input.password),
            full_name=input.full_name,
        )
        user = await self._user_repo.save(user)

        return UserOutput(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
        )
