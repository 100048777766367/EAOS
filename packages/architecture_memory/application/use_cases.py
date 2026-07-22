"""Use cases for Architecture Memory context."""

from packages.architecture_memory.application.dto import (
    MemoryRecordDTO,
    RecallMemoryQuery,
    StoreMemoryCommand,
)
from packages.architecture_memory.domain.models import (
    ArchitectureMemoryRecordAggregate,
    SemanticTag,
)
from packages.architecture_memory.domain.ports import (
    ArchitectureMemoryRepositoryPort,
    SemanticRecallPort,
)


class StoreArchitectureMemoryUseCase:
    def __init__(self, repository: ArchitectureMemoryRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: StoreMemoryCommand) -> None:
        record = ArchitectureMemoryRecordAggregate(
            memory_id=command.memory_id,
            tier=command.tier,
            memory_type=command.memory_type,
            title=command.title,
            context_summary=command.context_summary,
            lesson_learned=command.lesson_learned,
            linked_adr_id=command.linked_adr_id,
            confidence_score=command.confidence_score,
            tags=[SemanticTag(key=t.key, value=t.value) for t in command.tags],
        )

        self._repository.save(record)


class RecallArchitectureMemoryUseCase:
    """Queries institutional memory to prevent repeating past architectural mistakes."""

    def __init__(self, recall_port: SemanticRecallPort) -> None:
        self._recall_port = recall_port

    def execute(self, query: RecallMemoryQuery) -> list[MemoryRecordDTO]:
        recalled = self._recall_port.recall_relevant_memories(
            query_text=query.query_text,
            limit=query.limit,
            min_similarity=query.min_similarity,
        )

        return [
            MemoryRecordDTO(
                memory_id=record.memory_id,
                tier=record.tier,
                memory_type=record.memory_type,
                title=record.title,
                lesson_learned=record.lesson_learned,
                linked_adr_id=record.linked_adr_id,
                similarity_score=round(score, 4),
            )
            for record, score in recalled
        ]
