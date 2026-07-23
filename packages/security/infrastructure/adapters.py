"""Infrastructure storage adapters for Security context."""

from packages.security.domain.models import SecurityEntity


class InMemorySecurityRepository:
    """In-memory repository storing security entities."""

    def __init__(self) -> None:
        self._records: dict[str, SecurityEntity] = {}

    def save(self, entity: SecurityEntity) -> SecurityEntity:
        """Saves entity in memory."""
        self._records[entity.entity_id] = entity
        return entity

    def find_by_id(self, entity_id: str) -> SecurityEntity | None:
        """Finds entity by ID."""
        return self._records.get(entity_id)
