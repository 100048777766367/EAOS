"""Unit tests for Architecture Memory context."""


from packages.architecture_memory.application.dto import (
    RecallMemoryQuery,
    StoreMemoryCommand,
    TagDTO,
)
from packages.architecture_memory.application.use_cases import (
    RecallArchitectureMemoryUseCase,
    StoreArchitectureMemoryUseCase,
)
from packages.architecture_memory.domain.models import (
    MemoryTier,
    MemoryType,
)
from packages.architecture_memory.infrastructure.adapters import (
    InMemoryArchitectureMemoryRepository,
)


def test_store_and_recall_architecture_memory() -> None:
    repo = InMemoryArchitectureMemoryRepository()
    store_uc = StoreArchitectureMemoryUseCase(repo)
    recall_uc = RecallArchitectureMemoryUseCase(repo)

    # 1. Store past incident lesson regarding direct DB leakage
    store_uc.execute(
        StoreMemoryCommand(
            memory_id="MEM-101",
            tier=MemoryTier.EPISODIC,
            memory_type=MemoryType.INCIDENT_LESSON,
            title="Database Import Leak Incident",
            context_summary="Domain layer imported SQLAlchemy directly causing coupling.",
            lesson_learned="Always wrap database access behind Ports and Adapters.",
            linked_adr_id="ADR-004",
            confidence_score=0.95,
            tags=[
                TagDTO(key="rule", value="R4"),
                TagDTO(key="layer", value="domain"),
            ],
        )
    )

    # 2. Store irrelevant memory
    store_uc.execute(
        StoreMemoryCommand(
            memory_id="MEM-102",
            tier=MemoryTier.WORKING,
            memory_type=MemoryType.PATTERN_RULE,
            title="CSS Tailwind Config",
            context_summary="UI styling conventions.",
            lesson_learned="Use dark mode theme by default.",
            confidence_score=0.90,
        )
    )

    # 3. Recall memory: "Why shouldn't domain import database SQLAlchemy?"
    query = RecallMemoryQuery(
        query_text="domain import database SQLAlchemy coupling", limit=5
    )
    recalled_results = recall_uc.execute(query)

    assert len(recalled_results) >= 1
    top_memory = recalled_results[0]
    assert top_memory.memory_id == "MEM-101"
    assert top_memory.linked_adr_id == "ADR-004"
    assert "Ports and Adapters" in top_memory.lesson_learned
    assert top_memory.similarity_score > 0.0
