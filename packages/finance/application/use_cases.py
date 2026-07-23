"""Application use cases for Finance bounded context."""

from packages.finance.domain.models import (
    FinanceEntity,
    FinanceStatusVO,
)


class ExecuteFinanceUseCase:
    """Use case coordinating finance workflows."""

    def execute(self, entity_id: str) -> FinanceEntity:
        """Executes finance business operation."""
        status_vo = FinanceStatusVO(
            status_code="ACTIVE",
            is_active=True,
        )
        return FinanceEntity(
            entity_id=entity_id,
            name=f"finance-{entity_id}",
            status=status_vo,
        )
