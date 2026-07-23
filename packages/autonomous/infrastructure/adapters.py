"""Autonomous domain infrastructure repository adapters."""

from typing import Any


class InMemoryAutonomousRepository:
    """In-memory repository for autonomous loop cycles."""

    def __init__(self, db_url: str = "") -> None:
        self.db_url: str = db_url
        self._cycles: dict[str, Any] = {}

    def save(self, cycle: Any) -> Any:
        """Saves an autonomous loop cycle."""
        cycle_id = getattr(cycle, "id", str(len(self._cycles) + 1))
        self._cycles[cycle_id] = cycle
        return cycle

    def find_by_id(self, cycle_id: str) -> Any | None:
        """Retrieves cycle by ID."""
        return self._cycles.get(cycle_id)


class PostgresAutonomousRepository(InMemoryAutonomousRepository):
    """PostgreSQL adapter for autonomous domain persistence."""

    def __init__(self, db_url: str) -> None:
        super().__init__(db_url=db_url)
