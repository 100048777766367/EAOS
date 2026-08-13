from typing import Protocol

from packages.memory.domain.entities import MemoryRecord

"""Memory Domain Ports."""


class MemoryRepositoryPort(Protocol):
    """Repository Port for Memory Persistence."""

    def save(self, record: MemoryRecord) -> MemoryRecord:
        """Saves a memory record."""
        ...

    def get_by_id(self, record_id: str) -> MemoryRecord | None:
        """Retrieves a memory record by ID."""
        ...

    def find_by_id(self, record_id: str) -> MemoryRecord | None:
        """Retrieves a memory record by ID."""
        ...

    def list_all(self) -> list[MemoryRecord]:
        """Lists all stored memory records."""
        ...

    def search(
        self,
        query: str = "",
        limit: int = 10,
        user_id: str = "",
    ) -> list[MemoryRecord]:
        """Search memory records matching query string."""
        ...
