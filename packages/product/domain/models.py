from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Product & Pricing Catalog Domain Model for EAOS."""


class ProductCatalogItem(BaseModel):
    """Value object representing a digital product or service offering."""

    model_config = ConfigDict(frozen=True)

    product_id: str = Field(..., description="Unique Product ID")
    name: str = Field(..., description="Product display name")
    price_usd: float = Field(..., description="Product price in USD")
    product_type: str = Field(default="DIGITAL_TEMPLATE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
