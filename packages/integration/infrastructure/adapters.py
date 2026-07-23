"""Infrastructure storage adapters for Integration context."""

from packages.integration.domain.models import IntegrationEntity


class InMemoryIntegrationRepository:
    """In-memory repository storing integration entities."""

    def __init__(self) -> None:
        self._records: dict[str, IntegrationEntity] = {}

    def save(self, entity: IntegrationEntity) -> IntegrationEntity:
        """Saves entity in memory."""
        self._records[entity.entity_id] = entity
        return entity

    def find_by_id(self, entity_id: str) -> IntegrationEntity | None:
        """Finds entity by ID."""
        return self._records.get(entity_id)
