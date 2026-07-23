"""User domain entity for identity context."""

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    """Value object representing an identity user."""

    model_config = ConfigDict(frozen=True)

    id: str
    email: str
    username: str
    hashed_password: str = ""
