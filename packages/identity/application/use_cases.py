from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from pydantic import BaseModel, EmailStr

from packages.identity.domain.models import User
from packages.identity.domain.ports import UserRepository

"""Identity Application Use Cases (S-Tier Capability)."""


class RegisterUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterUserUseCase:
    """Use case đăng ký người dùng mới, mã hóa mật khẩu bằng bcrypt."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, request: RegisterUserRequest) -> User:
        existing_user = self.repository.find_by_email(request.email)
        if existing_user:
            raise ValueError(f"User with email {request.email} already exists")

        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(request.password.encode("utf-8"), salt).decode("utf-8")

        user = User(
            id=str(uuid.uuid4()),
            email=request.email,
            username=request.username.strip(),
            hashed_password=hashed_pw,
        )
        return self.repository.save(user)


class AuthenticateUserUseCase:
    """Use case xác thực người dùng và cấp JWT Token."""

    def __init__(self, repository: UserRepository, secret_key: str) -> None:
        self.repository = repository
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 60

    def execute(self, request: LoginRequest) -> TokenResponse:
        user = self.repository.find_by_email(request.email)
        if not user or not bcrypt.checkpw(request.password.encode("utf-8"), user.hashed_password.encode("utf-8")):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User is inactive")

        expire = datetime.now(UTC) + timedelta(minutes=self.access_token_expire_minutes)
        payload = {"sub": user.email, "exp": int(expire.timestamp())}
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        return TokenResponse(access_token=token)
