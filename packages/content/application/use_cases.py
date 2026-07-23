"""Application use cases for Content bounded context."""

from packages.content.domain.models import (
    ContentEntity,
    ContentStatusVO,
)


class ExecuteContentUseCase:
    """Use case coordinating content workflows."""

    def execute(self, entity_id: str) -> ContentEntity:
        """Executes content business operation."""
        status_vo = ContentStatusVO(
            status_code="ACTIVE",
            is_active=True,
        )
        return ContentEntity(
            entity_id=entity_id,
            name="content-$entity_id",
            status=status_vo,
        )
