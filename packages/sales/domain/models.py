from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Sales and Commerce Domain Model for EAOS Capability App."""


class SalesOrder(BaseModel):
    """Value object representing a customer digital order."""

    model_config = ConfigDict(frozen=True)

    order_id: str = Field(..., description="Unique Order UUID")
    customer_email: str = Field(..., description="Customer email")
    product_id: str = Field(..., description="Digital Product ID")
    amount_usd: float = Field(..., description="Order value in USD")
    status: str = Field(default="COMPLETED")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
