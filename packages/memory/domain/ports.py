from typing import Protocol

from packages.memory.domain.entities import MemoryRecord  # Sửa đường dẫn sang entities


class MemoryRepositoryPort(Protocol):
    """Port định nghĩa các hành vi truy vấn và ghi nhớ lịch sử."""

    def save(self, record: MemoryRecord) -> MemoryRecord: ...

    def find_by_id(self, record_id: str) -> MemoryRecord | None: ...

    def query_memories(self, keyword: str) -> list[MemoryRecord]: ...

    def vector_search(
        self, query_text: str, limit: int = 5
    ) -> list[MemoryRecord]: ...

    def list_all(self) -> list[MemoryRecord]: ...