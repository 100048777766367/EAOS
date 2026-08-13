from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from packages.evidence.domain.evidence import Evidence

"""Domain Model for Verified Evidence Bundle (Item 8 Filtered Fix)."""


class EvidenceBundleDTO(BaseModel):
    """Verified Evidence Bundle container filtered by explicit IDs."""

    model_config = ConfigDict(frozen=True)

    bundle_id: str = Field(..., description="Enterprise semantic model field description")
    query_text: str = Field(..., description="Enterprise semantic model field description")
    evidences: list[Evidence] = Field(default_factory=list)
    total_count: int = Field(default=0)
    chain_valid: bool = Field(default=True)
    tamper_detected: bool = Field(default=False)
