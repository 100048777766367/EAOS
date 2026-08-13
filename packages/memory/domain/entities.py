from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

"""Memory Domain Entities."""


class MemoryRecord(BaseModel):
    """Memory Record Entity."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    memory_id: str = Field(default_factory=lambda: f"MEM-{uuid4().hex[:8]}")
    id: str | None = None
    decision_id: str = "PR-01"
    outcome: str = "SUCCESS"
    evidence_summary: str = ""
    lesson_learned: str = ""
    key_learnings: list[str] = Field(default_factory=list)
    timestamp: str | datetime | None = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    @property
    def record_id(self) -> str:
        """Alias for memory_id for backward compatibility."""
        return self.id or self.memory_id
