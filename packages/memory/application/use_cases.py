import uuid
from datetime import UTC, datetime

from pydantic import BaseModel

from packages.memory.domain.entities import MemoryRecord  # Sửa đường dẫn sang entities
from packages.memory.domain.ports import MemoryRepositoryPort


class StoreMemoryRequest(BaseModel):
    decision_id: str
    outcome: str
    evidence_summary: str
    lesson_learned: str
    key_learnings: list[str]


class QueryMemoryUseCase:
    """Application Service chịu trách nhiệm hồi tưởng (Recall) bộ nhớ cũ."""

    def __init__(self, repo: MemoryRepositoryPort) -> None:
        self.repo = repo

    def recall(self, keyword: str) -> list[MemoryRecord]:
        return self.repo.query_memories(keyword)


class StoreMemoryUseCase:
    """Application Service điều phối lưu vết bộ nhớ mới."""

    def __init__(self, repo: MemoryRepositoryPort) -> None:
        self.repo = repo

    def execute(self, request: StoreMemoryRequest) -> MemoryRecord:
        mem_id = f"MEM-{uuid.uuid4().hex[:6].upper()}"
        record = MemoryRecord(
            id=mem_id,
            timestamp=datetime.now(UTC),
            decision_id=request.decision_id,
            outcome=request.outcome,
            evidence_summary=request.evidence_summary,
            lesson_learned=request.lesson_learned,
            key_learnings=request.key_learnings,
        )
        return self.repo.save(record)