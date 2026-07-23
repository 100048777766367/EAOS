"""Shared domain entity primitives and value objects for EAOS."""

from pydantic import BaseModel, ConfigDict


class EntityID(BaseModel):
    """Value object representing an immutable entity identifier."""

    model_config = ConfigDict(frozen=True)

    id_value: str


class EntityIdVO(EntityID):
    """Alias value object for entity identification."""
