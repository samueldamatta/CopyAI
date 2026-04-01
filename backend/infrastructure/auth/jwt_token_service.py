from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt


class JWTTokenService:
    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta if expires_delta else timedelta(minutes=self._expire_minutes)
        )
        to_encode["exp"] = expire
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
