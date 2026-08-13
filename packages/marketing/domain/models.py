from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

"""Marketing Capability Domain Models.

Hexagonal Rule: This module MUST NOT import from application/ or infrastructure/.
All models are pure value objects and entities with zero infrastructure coupling.
"""


# ---------------------------------------------------------------------------
# Enumerations — strongly-typed domain vocabulary
# ---------------------------------------------------------------------------

_SLUG_SEP: Final[str] = "-"


class MarketingChannel(StrEnum):
    """Supported omnichannel marketing delivery channels."""

    GOOGLE = "GOOGLE"
    FACEBOOK = "FACEBOOK"
    EMAIL = "EMAIL"
    LINKEDIN = "LINKEDIN"
    ORGANIC_SEO = "ORGANIC_SEO"


class ArticleStatus(StrEnum):
    """Lifecycle status of an SEO article draft."""

    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class CampaignStatus(StrEnum):
    """Lifecycle status of a marketing campaign."""

    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


# ---------------------------------------------------------------------------
# Value Objects — immutable, identity-free
# ---------------------------------------------------------------------------


class KeywordTarget(BaseModel):
    """Value object representing a researched SEO keyword target.

    Invariant: difficulty_score must be in [0.0, 100.0].
    """

    model_config = ConfigDict(frozen=True)

    keyword_id: str = Field(..., description="Unique Keyword ID (KW-XXXXXXXX)")
    keyword: str = Field(..., min_length=1, description="Search keyword text")
    search_volume: int = Field(default=0, ge=0, description="Monthly search volume")
    difficulty_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="SEO difficulty score 0–100",
    )

    @property
    def slug(self) -> str:
        """URL-safe slug derived from keyword text."""
        return self.keyword.lower().replace(" ", _SLUG_SEP)

    @property
    def is_low_competition(self) -> bool:
        """True when keyword difficulty is below 40 — good targeting signal."""
        return self.difficulty_score < 40.0


# ---------------------------------------------------------------------------
# Entities — have identity, may be mutable within aggregate boundary
# ---------------------------------------------------------------------------


class SEOArticleDraft(BaseModel):
    """Entity representing an AI-generated SEO article draft.

    Identity: article_id
    """

    model_config = ConfigDict(frozen=True)

    article_id: str = Field(..., description="Unique Article ID (ART-XXXXXXXX)")
    title: str = Field(..., min_length=1, description="Article title")
    slug: str = Field(..., min_length=1, description="SEO URL slug")
    keyword_id: str = Field(..., description="Target keyword ID reference")
    content_markdown: str = Field(..., description="Full body content in Markdown")
    status: ArticleStatus = Field(default=ArticleStatus.DRAFT)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def with_status(self, new_status: ArticleStatus) -> SEOArticleDraft:
        """Return a new draft with updated status (immutable update)."""
        return self.model_copy(update={"status": new_status})


class MarketingCampaign(BaseModel):
    """Entity representing an omnichannel marketing campaign.

    Identity: campaign_id
    """

    model_config = ConfigDict(frozen=True)

    campaign_id: str = Field(..., description="Unique Campaign ID (CAM-XXXXXXXX)")
    name: str = Field(..., min_length=1, description="Campaign display name")
    channel: MarketingChannel = Field(..., description="Delivery channel")
    content_asset_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description="References to associated content asset IDs",
    )
    status: CampaignStatus = Field(default=CampaignStatus.ACTIVE)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
