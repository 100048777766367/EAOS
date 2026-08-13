import uuid

from packages.manufacturing.domain.models import ProductionOrder

"""Application use cases for Manufacturing Order Execution."""


class ProcessProductionOrderUseCase:
    """Use case processing manufacturing order lifecycle."""

    def execute(self, product_sku: str, quantity: int) -> ProductionOrder:
        """Executes manufacturing production order creation."""
        order_id = f"MFG-{uuid.uuid4().hex[:8].upper()}"
        return ProductionOrder(
            order_id=order_id,
            product_sku=product_sku,
            quantity=quantity,
            status="IN_PROGRESS",
        )
