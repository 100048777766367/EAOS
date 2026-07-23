"""Application use cases for Security bounded context."""

from packages.security.domain.models import (
    SecurityEntity,
    SecurityStatusVO,
)


class ExecuteSecurityUseCase:
    """Use case coordinating security workflows."""

    def execute(self, entity_id: str) -> SecurityEntity:
        """Executes security business operation."""
        status_vo = SecurityStatusVO(
            status_code="ACTIVE",
            is_active=True,
        )
        return SecurityEntity(
            entity_id=entity_id,
            name="security-$entity_id",
            status=status_vo,
        )
