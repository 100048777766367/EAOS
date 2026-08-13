import uuid

from packages.sales.domain.models import SalesOrder

"""Application use cases for Sales Order Processing."""


class ProcessOrderUseCase:
    """Use case processing digital product order execution."""

    def execute(self, customer_email: str, product_id: str, amount_usd: float) -> SalesOrder:
        """Executes sales order creation workflow."""
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        return SalesOrder(
            order_id=order_id,
            customer_email=customer_email,
            product_id=product_id,
            amount_usd=amount_usd,
            status="COMPLETED",
        )
