"""Enterprise Domain Models and DTOs."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ActionProposalDTO(BaseModel):
    """DTO representing an agent action proposal."""

    model_config = ConfigDict(frozen=True)
    action_name: str = Field(..., description="Enterprise semantic model field description")
    action_type: str | None = Field(None, description="Enterprise semantic model field description")
    target: str | None = Field(None, description="Enterprise semantic model field description")
    target_uri: str | None = Field(None, description="Enterprise semantic model field description")
    parameters: dict[str, Any] = Field(default_factory=dict)
    is_destructive: bool = Field(default=False)


class VerifiedEvidenceBundleDTO(BaseModel):
    """DTO representing a verified bundle of evidences."""

    model_config = ConfigDict(frozen=True)
    bundle_id: str = Field(
        default="bundle-default",
        description="Enterprise semantic model field description",
    )
    query_text: str = Field(..., description="Enterprise semantic model field description")
    evidences: list[Any] = Field(default_factory=list)
    session_identity: str | None = Field(None, description="Enterprise semantic model field description")


class TurnMessageDTO(BaseModel):
    """DTO representing a single conversation turn message."""

    model_config = ConfigDict(frozen=True)
    turn_id: int = Field(..., description="Enterprise semantic model field description")
    session_id: str = Field(
        default="sess-default",
        description="Enterprise semantic model field description",
    )
    role: str = Field(..., description="Enterprise semantic model field description")
    content: str = Field(..., description="Enterprise semantic model field description")


class EntityNodeDTO(BaseModel):
    """DTO representing an entity node in the graph."""

    model_config = ConfigDict(frozen=True)
    entity_id: str = Field(..., description="Enterprise semantic model field description")
    name: str = Field(default="Entity", description="Enterprise semantic model field description")
    category: str = Field(default="general", description="Enterprise semantic model field description")


class ClaimValidityDTO:
    valid_to_turn: str | None = None


class _DummyClaimValidityDTO(BaseModel):
    """DTO representing claim validation details."""

    model_config = ConfigDict(frozen=True)
    claim_id: str = Field(..., description="Enterprise semantic model field description")
    statement: str = Field(..., description="Enterprise semantic model field description")
    is_valid: bool = Field(default=True, description="Enterprise semantic model field description")
    source_turn_id: int = Field(..., description="Enterprise semantic model field description")


class QueryPlanDTO(BaseModel):
    """DTO representing query execution planning."""

    model_config = ConfigDict(frozen=True)
    plan_id: str = Field(
        default="plan-default",
        description="Enterprise semantic model field description",
    )
    query_text: str = Field(..., description="Enterprise semantic model field description")
    time_priority: float = Field(default=0.5)
    relevance_score: float = Field(default=0.5)
    session_id: str | None = Field(None)
