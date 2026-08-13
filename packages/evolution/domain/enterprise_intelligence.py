from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

"""Enterprise Intelligence Economy Domain Models (v5.x)."""


class KnowledgeDNA(BaseModel):
    """DNA provenance metadata tracking origin and lineage of knowledge."""

    model_config = ConfigDict(frozen=True)

    origin_source: str = Field(..., description="Origin e.g. Incident")
    parent_asset_ids: list[str] = Field(default_factory=list)
    confidence_score: float = Field(default=1.0)
    valid_until: datetime | None = Field(default=None)
    version: str = Field(default="1.0.0")


class KnowledgeGravity(BaseModel):
    """Knowledge Gravity score based on usage, citation, and impact."""

    model_config = ConfigDict(frozen=True)

    reuse_count: int = Field(default=0)
    citation_count: int = Field(default=0)
    business_impact_score: float = Field(default=1.0)
    success_rate: float = Field(default=1.0)

    @property
    def gravity_score(self) -> float:
        """Calculate Knowledge Gravity score."""
        return (self.reuse_count + self.citation_count) * self.business_impact_score * self.success_rate


class EnterpriseIntelligenceAsset(BaseModel):
    """Strategic Enterprise Intelligence Asset (v5.x)."""

    model_config = ConfigDict(frozen=True)

    asset_id: str = Field(..., description="Unique intelligence ID")
    title: str = Field(..., description="Intelligence title")
    dna: KnowledgeDNA
    gravity: KnowledgeGravity
    natural_selection_rank: float = Field(default=1.0)
    is_standard: bool = Field(default=False)
    is_retired: bool = Field(default=False)
