from __future__ import annotations

from contexts.crm.crm_context import BoundedContextDTO

"""Sales Bounded Context Definition (DDD Pattern)."""


class SalesContextRegistry:
    """Registry providing Sales bounded context definition."""

    def get_context_dto(self) -> BoundedContextDTO:
        """Return Sales bounded context specification."""
        return BoundedContextDTO(
            context_id="sales",
            name="Sales & Order Processing",
            primary_entities=["Order", "Invoice", "Payment"],
            relationship="UPSTREAM_DOWNSTREAM",
        )
