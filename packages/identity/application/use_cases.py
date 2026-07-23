"""User registration and identity management use cases."""

import hashlib
from typing import Any

from pydantic import BaseModel, ConfigDict

from packages.identity.domain.models import User


class RegisterUserRequest(BaseModel):
    """DTO request model for user registration."""

    model_config = ConfigDict(frozen=True)

    email: str
    username: str
    password: str


class RegisterUserUseCase:
    """Use case processing user registration."""

    def __init__(self, user_repo: Any) -> None:
        self.user_repo = user_repo

    def execute(self, request: RegisterUserRequest) -> User:
        """Hashes password and persists user entity."""
        salt = f"eaos_salt_{request.username}"
        hashed_bytes = hashlib.pbkdf2_hmac(
            "sha256",
            request.password.encode("utf-8"),
            salt.encode("utf-8"),
            100000,
        )

        user_id = f"usr_{hash(request.email) & 0xFFFFFF:06x}"
        user = User(
            id=user_id,
            email=request.email,
            username=request.username,
            hashed_password=hashed_bytes.hex(),
        )
        self.user_repo.save(user)
        return user
