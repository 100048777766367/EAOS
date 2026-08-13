import uuid
from datetime import UTC, datetime

import structlog
from pydantic import BaseModel, ConfigDict, Field

from packages.memory.domain.entities import MemoryRecord
from packages.memory.domain.ports import MemoryRepositoryPort

"""Application Services for EAOS Memory Domain (CQRS Segregated)."""


logger = structlog.get_logger()


class StoreMemoryRequest(BaseModel):
    """Command DTO for storing a memory record."""

    model_config = ConfigDict(frozen=True)

    decision_id: str
    outcome: str
    evidence_summary: str
    lesson_learned: str
    key_learnings: list[str] = Field(default_factory=list)


class StoreMemoryUseCase:
    """Application Command Service for storing memory records."""

    def __init__(self, repo: MemoryRepositoryPort) -> None:
        self.repo = repo

    def execute(self, request: StoreMemoryRequest) -> MemoryRecord:
        """Stores a memory record with structured logging and generated ID."""
        record_id = f"MEM-{uuid.uuid4().hex[:8].upper()}"
        record = MemoryRecord(
            memory_id=record_id,
            timestamp=datetime.now(UTC),
            decision_id=request.decision_id,
            outcome=request.outcome,
            evidence_summary=request.evidence_summary,
            lesson_learned=request.lesson_learned,
            key_learnings=request.key_learnings,
        )
        saved_record = self.repo.save(record)
        logger.info(
            "Memory record stored successfully",
            memory_id=saved_record.memory_id,
            decision_id=saved_record.decision_id,
        )
        return saved_record


class QueryMemoryUseCase:
    """Application Query Service for memory retrieval."""

    def __init__(self, repo: MemoryRepositoryPort) -> None:
        self.repo = repo

    def get_by_id(self, memory_id: str) -> MemoryRecord | None:
        """Queries memory record by unique ID."""
        return self.repo.find_by_id(memory_id)

    def search(self, query: str, limit: int = 10) -> list[MemoryRecord]:
        """Queries memory records matching semantic or text query."""
        return self.repo.search(query=query, limit=limit)
