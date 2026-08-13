from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Enterprise Meta-Model Specifications (Sprint 3.1)."""


class AttributeMeta(BaseModel):
    """Attribute definition in Enterprise Meta-Model."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Attribute name")
    type_name: str = Field(..., description="Type e.g. string, UUID, int")
    required: bool = Field(default=True)


class EntityMeta(BaseModel):
    """Domain entity definition in Enterprise Meta-Model."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Entity name")
    attributes: list[AttributeMeta] = Field(default_factory=list)


class PolicyMeta(BaseModel):
    """Business policy rule definition in Enterprise Meta-Model."""

    model_config = ConfigDict(frozen=True)

    policy_id: str = Field(..., description="Unique policy ID")
    statement: str = Field(..., description="Policy rule statement")
    enforced: bool = Field(default=True)


class EventMeta(BaseModel):
    """Enterprise event definition in Enterprise Meta-Model."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Event name e.g. CustomerCreated")
    payload_schema: dict[str, Any] = Field(default_factory=dict)


class EnterpriseMetaModel(BaseModel):
    """Top-level Single Source of Truth Meta-Model (v1)."""

    model_config = ConfigDict(frozen=True)

    version: str = Field(default="1.0.0", description="DSL Version")
    enterprise_name: str = Field(..., description="Enterprise name")
    capabilities: list[str] = Field(default_factory=list)
    entities: list[EntityMeta] = Field(default_factory=list)
    policies: list[PolicyMeta] = Field(default_factory=list)
    events: list[EventMeta] = Field(default_factory=list)
