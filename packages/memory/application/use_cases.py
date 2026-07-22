import uuid
from datetime import UTC, datetime

from pydantic import BaseModel, Field

from packages.memory.domain.entities import MemoryRecord
from packages.memory.domain.ports import MemoryRepositoryPort


class StoreMemoryRequest(BaseModel):
    decision_id: str
    outcome: str
    evidence_summary: str
    lesson_learned: str
    key_learnings: list[str] = Field(default_factory=list)

class QueryMemoryUseCase:
    """Application Service quáº£n trá»‹ náº¡p vÃ  há»“i phÃ²ng tri thá»©c."""
    def __init__(self, repo: MemoryRepositoryPort) -> None:
        self.repo = repo

    def store_memory(self, request: StoreMemoryRequest) -> MemoryRecord:
        record_id = f"MEM-{uuid.uuid4().hex[:8].upper()}"
        record = MemoryRecord(
            id=record_id,
            timestamp=datetime.now(UTC),
            decision_id=request.decision_id,
            outcome=request.outcome,
            evidence_summary=request.evidence_summary,
            lesson_learned=request.lesson_learned,
            key_learnings=request.key_learnings
        )
        return self.repo.save(record)

