from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from packages.evidence.domain.evidence_status import EvidenceStatus

"""Domain Model for Bound Cryptographic Evidence Canonical Hash & Chain."""


class EvidenceIntegrityDTO(BaseModel):
    """Bound Cryptographic canonical hash chain tracking DTO."""

    model_config = ConfigDict(frozen=True)

    algorithm: str = Field(default="SHA-256")
    canonical_hash: str = Field(..., description="Enterprise semantic model field description")
    previous_hash: str | None = Field(default=None)
    chain_hash: str = Field(..., description="Enterprise semantic model field description")
    status: EvidenceStatus = Field(default=EvidenceStatus.CAPTURED)
