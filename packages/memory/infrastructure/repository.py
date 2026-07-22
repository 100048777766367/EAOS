from packages.memory.domain.entities import MemoryRecord
from packages.memory.domain.ports import MemoryRepositoryPort


class InMemoryMemoryRepository(MemoryRepositoryPort):
    def __init__(self) -> None:
        self._store: dict[str, MemoryRecord] = {}

    def save(self, record: MemoryRecord) -> MemoryRecord:
        self._store[record.id] = record
        return record

    def find_by_id(self, memory_id: str) -> MemoryRecord | None:
        return self._store.get(memory_id)

    def list_all(self) -> list[MemoryRecord]:
        return list(self._store.values())

    def vector_search(self, query: str, limit: int = 5) -> list[MemoryRecord]:
        query_tokens = query.lower().split()
        results = []
        for record in self._store.values():
            text_space = (f"{record.lesson_learned} {record.evidence_summary} {' '.join(record.key_learnings)}").lower()
            overlap = sum(1 for t in query_tokens if t in text_space)
            if overlap > 0:
                results.append((overlap, record))
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]

    def query_memories(self, keyword: str) -> list[MemoryRecord]:
        k = keyword.lower()
        results = []
        for record in self._store.values():
            in_lesson = k in record.lesson_learned.lower()
            in_evidence = k in record.evidence_summary.lower()
            in_keys = any(k in kl.lower() for kl in record.key_learnings)
            if in_lesson or in_evidence or in_keys:
                results.append(record)
        return results
