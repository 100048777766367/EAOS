import uuid

from packages.memory.application.dto import MemoryResponse, StoreMemoryCommand
from packages.memory.domain.entities import MemoryRecord
from packages.memory.domain.ports import MemoryRepositoryPort

"""Memory Application Handlers."""


class StoreMemoryHandler:
    """Handler processing memory storage commands."""

    def __init__(self, repo: MemoryRepositoryPort) -> None:
        self.repo = repo

    def handle(self, cmd: StoreMemoryCommand) -> MemoryResponse:
        """Processes StoreMemoryCommand and returns MemoryResponse."""
        rec_id = f"MEM-{uuid.uuid4().hex[:8].upper()}"
        rec = MemoryRecord(
            memory_id=rec_id,
            decision_id=cmd.decision_id,
            outcome=cmd.outcome,
            evidence_summary=cmd.evidence_summary,
            lesson_learned=cmd.lesson_learned,
            key_learnings=cmd.key_learnings,
        )
        self.repo.save(rec)
        return MemoryResponse(
            id=rec.memory_id,
            outcome=cmd.outcome,
            lesson_learned=cmd.lesson_learned,
            message="Memory record stored successfully",
        )
