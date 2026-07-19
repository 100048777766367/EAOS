from packages.memory.domain.entities import MemoryRecord  # Sửa đường dẫn sang entities
from packages.memory.domain.ports import MemoryRepositoryPort


class InMemoryMemoryRepository(MemoryRepositoryPort):
    """Adapter lưu trữ bộ nhớ mỏng trong RAM (Không chứa Retry/Telemetry)."""

    def __init__(self) -> None:
        self.working_memory: list[MemoryRecord] = []
        self.long_term_memory: dict[str, MemoryRecord] = {}

    def save(self, record: MemoryRecord) -> MemoryRecord:
        if len(self.working_memory) >= 10:
            self.working_memory.pop(0)
        self.working_memory.append(record)

        self.long_term_memory[record.id] = record
        return record

    def find_by_id(self, record_id: str) -> MemoryRecord | None:
        return self.long_term_memory.get(record_id)

    def query_memories(self, keyword: str) -> list[MemoryRecord]:
        k = keyword.lower()
        results = []
        for record in self.long_term_memory.values():
            in_lesson = k in record.lesson_learned.lower()
            in_evidence = k in record.evidence_summary.lower()
            in_keys = any(k in kl.lower() for kl in record.key_learnings)
            if in_lesson or in_evidence or in_keys:
                results.append(record)
        return results

    def vector_search(
        self, query_text: str, limit: int = 5
    ) -> list[MemoryRecord]:
        """Thuật toán Jaccard mô phỏng tìm kiếm Vector lọc nhiễu."""
        query_words = set(query_text.lower().split())
        scored_records = []

        for record in self.long_term_memory.values():
            combined_text = (
                f"{record.lesson_learned} {record.evidence_summary} "
                f"{' '.join(record.key_learnings)}"
            )
            record_words = set(combined_text.lower().split())

            intersection = query_words.intersection(record_words)
            union = query_words.union(record_words)
            similarity = len(intersection) / len(union) if union else 0.0

            scored_records.append((similarity, record))

        sorted_records = sorted(
            scored_records, key=lambda x: x[0], reverse=True
        )
        return [
            record
            for score, record in sorted_records[:limit]
            if score >= 0.15
        ]

    def list_all(self) -> list[MemoryRecord]:
        return list(self.long_term_memory.values())