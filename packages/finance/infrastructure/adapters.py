"""Infrastructure storage adapters for Finance context."""

from packages.finance.domain.models import FinanceEntity


class InMemoryFinanceRepository:
    """In-memory repository storing finance entities."""

    def __init__(self) -> None:
        self._records: dict[str, FinanceEntity] = {}

    def save(self, entity: FinanceEntity) -> FinanceEntity:
        """Saves entity in memory."""
        self._records[entity.entity_id] = entity
        return entity

    def find_by_id(self, entity_id: str) -> FinanceEntity | None:
        """Finds entity by ID."""
        return self._records.get(entity_id)
