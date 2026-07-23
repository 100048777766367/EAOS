"""Infrastructure storage adapters for Automation context."""

from packages.automation.domain.models import AutomationEntity


class InMemoryAutomationRepository:
    """In-memory repository storing automation entities."""

    def __init__(self) -> None:
        self._records: dict[str, AutomationEntity] = {}

    def save(self, entity: AutomationEntity) -> AutomationEntity:
        """Saves entity in memory."""
        self._records[entity.entity_id] = entity
        return entity

    def find_by_id(self, entity_id: str) -> AutomationEntity | None:
        """Finds entity by ID."""
        return self._records.get(entity_id)
