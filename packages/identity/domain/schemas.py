from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr, Field

"""Identity domain schemas and DTOs."""


__all__ = ["UserRegisterRequest", "UserResponse", "UserRole"]


class UserRole(StrEnum):
    ADMIN = "admin"
    OPERATOR = "operator"
    AGENT = "agent"


class UserRegisterRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: EmailStr
    username: str | None = None
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default="AI Agent", min_length=1, max_length=255)


class UserResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    email: EmailStr
    full_name: str
    role: UserRole
