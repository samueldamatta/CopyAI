import hashlib

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    def _prepare(self, password: str) -> str:
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            return hashlib.sha256(password_bytes).hexdigest()
        return password

    def hash(self, password: str) -> str:
        return _pwd_context.hash(self._prepare(password))

    def verify(self, plain: str, hashed: str) -> bool:
        return _pwd_context.verify(self._prepare(plain), hashed)
