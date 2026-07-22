from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    """Domain Entity Ä‘áº¡i diá»‡n cho ngÆ°á»i dÃ¹ng (Con ngÆ°á»i hoáº·c AI Agent)."""

    id: str | None = Field(default=None)
    email: EmailStr = Field(...)
    username: str = Field(...)
    hashed_password: str = Field(...)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
