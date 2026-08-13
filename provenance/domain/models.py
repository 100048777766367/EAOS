"""Domain Models for Provenance Engine."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ClaimValidityDTO(BaseModel):
    """DTO representing claim validity check."""

    model_config = ConfigDict(frozen=True)
    claim_id: str = Field(default="claim-default", description="Claim identifier")
    subject: str = Field(default="default-subject", description="Claim subject")
    predicate: str = Field(default="default-predicate", description="Claim predicate")
    object_val: str = Field(default="default-object", description="Claim object value")
    is_valid: bool = Field(default=True, description="Claim validity status")
    confidence: float = Field(default=1.0, description="Confidence score")
    valid_from_turn: int = Field(default=0, description="Valid from turn id")
    valid_to_turn: int | None = Field(default=None, description="Valid to turn id")
    source_turn_id: int = Field(default=0, description="Source turn id")


class VerifiedEvidenceBundleDTO(BaseModel):
    """DTO representing verified evidence bundle."""

    model_config = ConfigDict(frozen=True)
    bundle_id: str = Field(
        default="bundle-default",
        description="Enterprise semantic model field description",
    )
    evidences: list[str] = Field(default_factory=list, description="Enterprise semantic model field description")


class EntityNodeDTO(BaseModel):
    """DTO representing an entity node in deterministic graph."""

    model_config = ConfigDict(frozen=True)
    entity_id: str = Field(default="ent-default", description="Entity identifier")
    entity_type: str = Field(default="generic", description="Entity type")
    attributes: dict[str, str] = Field(default_factory=dict, description="Attributes mapping")
    name: str = Field(default="Entity", description="Human readable name")


class QueryPlanDTO(BaseModel):
    """DTO representing structured retrieval query plan."""

    model_config = ConfigDict(frozen=True)
    plan_id: str = Field(default="plan-default", description="Plan identifier")
    target_entities: list[str] = Field(default_factory=list, description="Target entities")
    filters: dict[str, str] = Field(default_factory=dict, description="Filters mapping")
    time_priority: float = Field(default=0.0, description="Time priority weight")
    relation_priority: float = Field(default=0.0, description="Relation priority weight")


class RelationEdgeDTO(BaseModel):
    """DTO representing a relationship edge between entity nodes."""

    model_config = ConfigDict(frozen=True)
    source_id: str = Field(default="src-default", description="Source node id")
    target_id: str = Field(default="tgt-default", description="Target node id")
    relation_type: str = Field(default="rel-default", description="Relation type")
    weight: float = Field(default=1.0, description="Edge weight")


class TurnMessageDTO(BaseModel):
    """DTO representing a turn message for processing."""

    model_config = ConfigDict(frozen=True)
    message_id: str = Field(default="msg-default", description="Message identifier")
    session_id: str = Field(default="sess-default", description="Session identifier")
    turn_id: int = Field(default=0, description="Turn sequence number")
    role: str = Field(default="user", description="Role of the sender")
    content: str = Field(default="", description="Content message")


class VerifiedContextDTO(BaseModel):
    """DTO representing verified context bundle."""

    model_config = ConfigDict(frozen=True)
    query_text: str = Field(default="", description="Original query text")
    claims: list[Any] = Field(default_factory=list, description="Active claims")
    turns: list[Any] = Field(default_factory=list, description="Conversation turns")
    citations: list[str] = Field(default_factory=list, description="Provenance citations")
    llm_tokens_spent_indexing: int = Field(default=0, description="Tokens spent indexing")
    llm_tokens_spent_retrieval: int = Field(default=0, description="Tokens spent retrieval")
    context_id: str = Field(default="ctx-default", description="Context identifier")
    verified_data: str = Field(default="", description="Verified data payload")
    trust_score: float = Field(default=1.0, description="Trust score")
