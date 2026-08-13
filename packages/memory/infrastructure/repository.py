from packages.memory.domain.entities import MemoryRecord

"""InMemory Memory Repository implementation."""


class InMemoryMemoryRepository:
    """In-memory implementation of memory repository matching MemoryRepositoryPort."""

    def __init__(self) -> None:
        self._storage: dict[str, MemoryRecord] = {}

    def save(self, memory: MemoryRecord) -> MemoryRecord:
        """Saves a memory record matching protocol parameter name."""
        rec_id = getattr(memory, "memory_id", getattr(memory, "id", "default_id"))
        self._storage[rec_id] = memory
        return memory

    def get_by_id(self, memory_id: str) -> MemoryRecord | None:
        """Retrieves a memory record by ID."""
        return self._storage.get(memory_id)

    def find_by_id(self, memory_id: str) -> MemoryRecord | None:
        """Retrieves a memory record by ID for Protocol compatibility."""
        return self._storage.get(memory_id)

    def list_all(self) -> list[MemoryRecord]:
        """Returns all stored memory records."""
        return list(self._storage.values())

    def search(
        self,
        query: str = "",
        limit: int = 10,
        user_id: str = "",
    ) -> list[MemoryRecord]:
        """Search memory records matching query string."""
        results: list[MemoryRecord] = []
        q = query.lower()
        for record in self._storage.values():
            if not q or q in record.lesson_learned.lower() or q in record.evidence_summary.lower():
                results.append(record)
            if len(results) >= limit:
                break
        return results
