from typing import Any

from fastapi import APIRouter
from packages.sales.application.use_cases import ProcessOrderUseCase
from pydantic import BaseModel, ConfigDict

"""FastAPI Router for Sales Capability Application."""


router = APIRouter(prefix="/v1/sales", tags=["Sales Capability"])


class ProcessOrderRequest(BaseModel):
    """Value object representing digital order payload."""

    model_config = ConfigDict(frozen=True)

    customer_email: str
    product_id: str
    amount_usd: float


@router.post("/orders/process")
async def process_order(request: ProcessOrderRequest) -> dict[str, Any]:
    """Processes digital product order execution."""
    use_case = ProcessOrderUseCase()
    order = use_case.execute(request.customer_email, request.product_id, request.amount_usd)
    return order.model_dump()
