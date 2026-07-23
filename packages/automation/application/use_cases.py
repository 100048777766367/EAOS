"""Application use cases for Automation bounded context."""

from packages.automation.domain.models import (
    AutomationEntity,
    AutomationStatusVO,
)


class ExecuteAutomationUseCase:
    """Use case coordinating automation workflows."""

    def execute(self, entity_id: str) -> AutomationEntity:
        """Executes automation business operation."""
        status_vo = AutomationStatusVO(
            status_code="ACTIVE",
            is_active=True,
        )
        return AutomationEntity(
            entity_id=entity_id,
            name="automation-$entity_id",
            status=status_vo,
        )
