import uuid
from datetime import UTC, datetime

from packages.memory.application.dto import MemoryResponse, StoreMemoryCommand
from packages.memory.domain.entities import MemoryRecord
from packages.memory.domain.ports import MemoryRepositoryPort


class StoreMemoryHandler:
    """Handler chá»‹u trÃ¡ch nhiá»‡m thá»±c thi nghiá»‡p vá»¥ lÆ°u váº¿t bá»™ nhá»›."""

    def __init__(self, repo: MemoryRepositoryPort) -> None:
        self.repo = repo

    def handle(self, command: StoreMemoryCommand) -> MemoryResponse:
        mem_id = f"MEM-{uuid.uuid4().hex[:6].upper()}"
        record = MemoryRecord(
            id=mem_id,
            memory_type="EPISODIC",
            timestamp=datetime.now(UTC),
            decision_id=command.decision_id,
            outcome=command.outcome,
            evidence_summary=command.evidence_summary,
            lesson_learned=command.lesson_learned,
            key_learnings=command.key_learnings,
        )
        saved = self.repo.save(record)
        return MemoryResponse(
            id=saved.id,
            outcome=saved.outcome,
            lesson_learned=saved.lesson_learned,
        )


class RecallMemoryHandler:
    """Handler chá»‹u trÃ¡ch nhiá»‡m thá»±c thi há»“i tÆ°á»Ÿng bá»™ nhá»›."""

    def __init__(self, repo: MemoryRepositoryPort) -> None:
        self.repo = repo

    def query(self, keyword: str) -> list[MemoryRecord]:
        return self.repo.query_memories(keyword)

    def semantic_recall(self, query_text: str, limit: int = 5) -> list[MemoryRecord]:
        return self.repo.vector_search(query_text, limit)
