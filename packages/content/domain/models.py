import uuid
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Content Capability Domain Models for EAOS Digital Assets."""


class ContentStatusVO(BaseModel):
    """Value Object representing content status details."""

    model_config = ConfigDict(frozen=True)

    status_code: str = Field(default="DRAFT")
    is_active: bool = Field(default=True)


class DigitalContentAsset(BaseModel):
    """Entity representing a reusable digital content asset."""

    model_config = ConfigDict(frozen=True)

    asset_id: str = Field(
        default_factory=lambda: f"CNT-{uuid.uuid4().hex[:8].upper()}",
        description="Unique Asset ID",
    )
    entity_id: str = Field(default="", description="Entity identifier")
    name: str = Field(default="", description="Content name")
    title: str = Field(default="", description="Asset title")
    asset_type: str = Field(default="ARTICLE", description="ARTICLE, VIDEO, EBOOK")
    body_markdown: str = Field(default="", description="Content body")
    status: ContentStatusVO | str = Field(default_factory=lambda: ContentStatusVO())
    repurposed_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @property
    def content_id(self) -> str:
        """Alias for content ID."""
        return self.entity_id or self.asset_id


# Alias for legacy infrastructure adapters compatibility
ContentEntity = DigitalContentAsset
