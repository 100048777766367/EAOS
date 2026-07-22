"""Domain models for Architecture Memory context."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, auto


class MemoryTier(Enum):
    WORKING = auto()
    EPISODIC = auto()
    SEMANTIC = auto()


class MemoryType(Enum):
    INCIDENT_LESSON = auto()
    ADR_RATIONALE = auto()
    TRADE_OFF = auto()
    PATTERN_RULE = auto()


@dataclass(frozen=True, slots=True)
class SemanticTag:
    key: str
    value: str


@dataclass(slots=True)
class ArchitectureMemoryRecordAggregate:
    memory_id: str
    tier: MemoryTier
    memory_type: MemoryType
    title: str
    context_summary: str
    lesson_learned: str
    linked_adr_id: str | None = None
    confidence_score: float = 1.0  # 0.0 -> 1.0
    tags: list[SemanticTag] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def calculate_similarity(self, query_tokens: set[str]) -> float:
        """Calculates Jaccard Index similarity against record tokens."""
        content_text = (
            f"{self.title} {self.context_summary} {self.lesson_learned} {' '.join(t.value for t in self.tags)}"
        ).lower()

        record_tokens = set(content_text.split())
        if not record_tokens or not query_tokens:
            return 0.0

        intersection = record_tokens.intersection(query_tokens)
        union = record_tokens.union(query_tokens)
        return len(intersection) / len(union)

    def promote_to_semantic(self) -> bool:
        """Promotes episodic memory to permanent semantic memory if confidence is high."""
        if self.confidence_score >= 0.8:
            self.tier = MemoryTier.SEMANTIC
            return True
        return False
