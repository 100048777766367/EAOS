from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Marketing Application DTOs — Input Commands and Output Results.

Hexagonal Rule: DTOs live in the application layer as the boundary contract.
They translate between external representations and domain objects.
They MUST NOT contain business logic.
"""


# ---------------------------------------------------------------------------
# Input Command DTOs (inbound from primary adapters / driving side)
# ---------------------------------------------------------------------------


class KeywordResearchCommand(BaseModel):
    """Command DTO to trigger keyword research workflow."""

    model_config = ConfigDict(frozen=True)

    keyword_text: str = Field(..., min_length=1, description="Raw keyword string to research")
    locale: str = Field(default="en-US", description="BCP-47 locale tag for market targeting")


class ArticleGenerationCommand(BaseModel):
    """Command DTO to trigger SEO article generation workflow."""

    model_config = ConfigDict(frozen=True)

    title: str = Field(..., min_length=1, description="Desired article headline")
    keyword_id: str = Field(..., description="ID of a previously researched keyword")
    word_count: int = Field(default=800, ge=100, le=5000, description="Target word count")


class CampaignLaunchCommand(BaseModel):
    """Command DTO to launch an omnichannel marketing campaign."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=1, description="Campaign display name")
    channel: str = Field(..., description="Target channel: GOOGLE, FACEBOOK, EMAIL, etc.")
    content_asset_ids: list[str] = Field(
        default_factory=list,
        description="References to associated content asset IDs",
    )


# ---------------------------------------------------------------------------
# Output Result DTOs (outbound to primary adapters / driving side)
# ---------------------------------------------------------------------------


class KeywordResearchResult(BaseModel):
    """Result DTO carrying keyword research outcomes."""

    model_config = ConfigDict(frozen=True)

    keyword_id: str = Field(..., description="Assigned keyword ID")
    keyword: str = Field(..., description="Researched keyword text")
    slug: str = Field(..., description="URL-safe slug")
    search_volume: int = Field(..., description="Monthly search volume")
    difficulty_score: float = Field(..., description="SEO difficulty score 0–100")
    is_low_competition: bool = Field(..., description="True when difficulty < 40")


class ArticleResult(BaseModel):
    """Result DTO carrying article draft outcomes."""

    model_config = ConfigDict(frozen=True)

    article_id: str = Field(..., description="Assigned article ID")
    title: str = Field(..., description="Article headline")
    slug: str = Field(..., description="URL slug derived from keyword")
    keyword_id: str = Field(..., description="Associated keyword ID")
    status: str = Field(..., description="Article lifecycle status")
    content_preview: str = Field(..., description="First 200 chars of content")


class CampaignResult(BaseModel):
    """Result DTO carrying campaign creation outcomes."""

    model_config = ConfigDict(frozen=True)

    campaign_id: str = Field(..., description="Assigned campaign ID")
    name: str = Field(..., description="Campaign name")
    channel: str = Field(..., description="Delivery channel")
    status: str = Field(..., description="Campaign lifecycle status")
    content_asset_count: int = Field(..., description="Number of linked content assets")
