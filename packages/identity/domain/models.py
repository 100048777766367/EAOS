from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    """Domain Entity đại diện cho người dùng (Con người hoặc AI Agent)."""

    id: str | None = Field(default=None)
    email: EmailStr = Field(...)
    username: str = Field(...)
    hashed_password: str = Field(...)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
