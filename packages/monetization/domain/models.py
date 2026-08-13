from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Monetization & Usage-Based Billing Domain Models for EAOS."""


class TokenUsageLedgerEntry(BaseModel):
    """Value object representing an API/LLM usage transaction."""

    model_config = ConfigDict(frozen=True)

    transaction_id: str
    tenant_id: str
    capability_used: str
    prompt_tokens: int
    completion_tokens: int
    charge_usd: float
    is_paid: bool = True
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CommunityPackManifest(BaseModel):
    """Entity representing a community-contributed Capability Pack."""

    model_config = ConfigDict(frozen=True)

    pack_id: str
    pack_name: str
    author_developer: str
    price_per_use_usd: float = 0.01
    royalty_share_ratio: float = 0.70
    version: str = "1.0.0"
