"""Application use cases for Integration bounded context."""

from packages.integration.domain.models import (
    IntegrationEntity,
    IntegrationStatusVO,
)


class ExecuteIntegrationUseCase:
    """Use case coordinating integration workflows."""

    def execute(self, entity_id: str) -> IntegrationEntity:
        """Executes integration business operation."""
        status_vo = IntegrationStatusVO(
            status_code="ACTIVE",
            is_active=True,
        )
        return IntegrationEntity(
            entity_id=entity_id,
            name="integration-$entity_id",
            status=status_vo,
        )
