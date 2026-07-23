"""Infrastructure adapters for evolution domain repositories."""

from typing import Any


class InMemoryEvolutionRepository:
    """In-memory repository for evolution objects and lineage."""

    def __init__(self) -> None:
        self._records: dict[str, Any] = {}

    def save(self, obj: Any) -> Any:
        """Saves an evolution object."""
        obj_id = getattr(obj, "id", str(len(self._records) + 1))
        self._records[obj_id] = obj
        return obj

    def find_by_id(self, doc_id: str) -> Any | None:
        """Finds an evolution object by ID."""
        return self._records.get(doc_id)

    def get_lineage(self, doc_id: str) -> list[str]:
        """Gets evolution document lineage IDs."""
        return [doc_id]


class PostgresEvolutionRepository(InMemoryEvolutionRepository):
    """PostgreSQL adapter for evolution domain persistence."""

    def __init__(self, db_url: str) -> None:
        super().__init__()
        self.db_url: str = db_url
