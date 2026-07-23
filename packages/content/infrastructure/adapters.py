"""Infrastructure storage adapters for Content context."""

from packages.content.domain.models import ContentEntity


class InMemoryContentRepository:
    """In-memory repository storing content entities."""

    def __init__(self) -> None:
        self._records: dict[str, ContentEntity] = {}

    def save(self, entity: ContentEntity) -> ContentEntity:
        """Saves entity in memory."""
        self._records[entity.entity_id] = entity
        return entity

    def find_by_id(self, entity_id: str) -> ContentEntity | None:
        """Finds entity by ID."""
        return self._records.get(entity_id)
