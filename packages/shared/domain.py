"""Shared DDD domain primitives and base value object abstractions."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class ValueObjectBase(BaseModel):
    """Immutable base value object for all DDD packages."""

    model_config = ConfigDict(frozen=True)


class DomainEventBase(BaseModel):
    """Immutable base domain event for EAOS Event Mesh."""

    model_config = ConfigDict(frozen=True)

    event_id: str
    timestamp: str
    payload: dict[str, Any]
