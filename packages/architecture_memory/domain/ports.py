"""Domain ports for Architecture Memory context."""

from typing import Protocol

from packages.architecture_memory.domain.models import (
    ArchitectureMemoryRecordAggregate,
)


class ArchitectureMemoryRepositoryPort(Protocol):
    def save(self, record: ArchitectureMemoryRecordAggregate) -> None:
        ...

    def find_by_id(
        self, memory_id: str
    ) -> ArchitectureMemoryRecordAggregate | None:
        ...

    def list_all(self) -> list[ArchitectureMemoryRecordAggregate]:
        ...


class SemanticRecallPort(Protocol):
    def recall_relevant_memories(
        self, query_text: str, limit: int = 5, min_similarity: float = 0.1
    ) -> list[tuple[ArchitectureMemoryRecordAggregate, float]]:
        ...
