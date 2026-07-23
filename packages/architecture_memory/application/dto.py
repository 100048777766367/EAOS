"""DTOs for Architecture Memory application layer."""

from pydantic import BaseModel, Field

from packages.architecture_memory.domain.models import MemoryTier, MemoryType


class TagDTO(BaseModel):
    key: str
    value: str


class StoreMemoryCommand(BaseModel):
    memory_id: str
    tier: MemoryTier
    memory_type: MemoryType
    title: str
    context_summary: str
    lesson_learned: str
    linked_adr_id: str | None = None
    confidence_score: float = 1.0
    tags: list[TagDTO] = Field(default_factory=list)


class RecallMemoryQuery(BaseModel):
    query_text: str
    limit: int = 5
    min_similarity: float = 0.05


class MemoryRecordDTO(BaseModel):
    memory_id: str
    tier: MemoryTier
    memory_type: MemoryType
    title: str
    lesson_learned: str
    linked_adr_id: str | None
    similarity_score: float
