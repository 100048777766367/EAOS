from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Knowledge Economy & Asset Valuation Domain Models (100-Year Life)."""


class KnowledgeLifecycleState(StrEnum):
    """Lifecycle states for Enterprise Knowledge Assets."""

    ACTIVE = "ACTIVE"
    HISTORICAL = "HISTORICAL"
    ARCHIVED = "ARCHIVED"
    RETIRED = "RETIRED"
    DESTROYED = "DESTROYED"


class KnowledgeValuation(BaseModel):
    """Asset valuation metadata for enterprise knowledge."""

    model_config = ConfigDict(frozen=True)

    asset_id: str = Field(..., description="Unique knowledge asset ID")
    category: str = Field(default="BUSINESS", description="Open taxonomy")
    confidence_score: float = Field(default=1.0)
    importance_score: float = Field(default=1.0)
    business_impact: float = Field(default=1.0)
    maintenance_cost: float = Field(default=0.1)
    reuse_count: int = Field(default=0)
    lifecycle_state: KnowledgeLifecycleState = Field(default=KnowledgeLifecycleState.ACTIVE)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_used_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class KnowledgeLifecycleDecision(BaseModel):
    """Action decision for a knowledge asset based on valuation."""

    model_config = ConfigDict(frozen=True)

    asset_id: str
    action: str = Field(..., description="KEEP, ARCHIVE, MERGE, FORGET")
    utility_score: float
    reasoning: str
