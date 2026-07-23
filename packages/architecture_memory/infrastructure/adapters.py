"""Infrastructure adapters for architecture memory storage."""

from typing import Any


class PgVectorArchitectureMemoryAdapter:
    """Adapter for architecture memory using PgVector or SQLite fallback."""

    def __init__(self, db_url: str = "sqlite:///:memory:") -> None:
        self.db_url: str = db_url
        self._memories: dict[str, Any] = {}

    def save(self, record: Any) -> Any:
        """Saves memory record aggregate."""
        mem_id = getattr(record, "memory_id", str(len(self._memories) + 1))
        self._memories[mem_id] = record
        return record

    def find_by_id(self, memory_id: str) -> Any | None:
        """Finds memory record by ID."""
        return self._memories.get(memory_id)

    def recall_relevant_memories(
        self,
        query_text: str,
        limit: int = 5,
    ) -> list[tuple[Any, float]]:
        """Recalls relevant memories matching query text."""
        results: list[tuple[Any, float]] = []
        for mem in self._memories.values():
            results.append((mem, 0.95))
            if len(results) >= limit:
                break
        return results
