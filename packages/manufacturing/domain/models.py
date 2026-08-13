from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Manufacturing & Supply Chain Domain Model for EAOS Capability App."""


class ProductionOrder(BaseModel):
    """Value object representing a manufacturing production order."""

    model_config = ConfigDict(frozen=True)

    order_id: str = Field(..., description="Unique Order UUID")
    product_sku: str = Field(..., description="Product Stock Keeping Unit")
    quantity: int = Field(..., description="Units to manufacture")
    status: str = Field(default="PLANNED")
    scheduled_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
