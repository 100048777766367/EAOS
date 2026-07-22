from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class MemoryRecord(BaseModel):
    """Thực thể bản ghi bộ nhớ vĩnh cửu trong RAM."""

    id: str = Field(..., description="Mã bản ghi")
    memory_type: str = Field(default="EPISODIC", description="Phân loại bộ nhớ")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    decision_id: str = Field(..., description="Mã quyết định")
    outcome: str = Field(..., description="Kết quả")
    evidence_summary: str = Field(..., description="Bằng chứng")
    lesson_learned: str = Field(..., description="Bài học")
    key_learnings: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)
