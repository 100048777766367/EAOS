from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

"""Business Capability Service Executable Example."""


class ServiceExampleResultDTO(BaseModel):
    """Result DTO for Business Capability service example."""

    model_config = ConfigDict(frozen=True)

    capability_id: str
    discount_amount: Decimal
    status: str = Field(default="COMPLETED")


def run_service_example(order_total: Decimal) -> ServiceExampleResultDTO:
    """Execute Sales Discount Business Capability example."""
    discount = min(order_total * Decimal("0.25"), Decimal(3000000))
    return ServiceExampleResultDTO(
        capability_id="sales_discount",
        discount_amount=discount,
        status="COMPLETED",
    )
