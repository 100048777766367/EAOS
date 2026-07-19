from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class MemoryRecord(BaseModel):
    """Domain Entity đại diện cho một bản ghi bộ nhớ vĩnh cửu."""

    id: str = Field(..., description="Mã bản ghi bộ nhớ")
    memory_type: str = Field(..., description="EPISODIC hoặc SEMANTIC")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    decision_id: str = Field(..., description="Mã quyết định liên kết")
    outcome: str = Field(..., description="Kết quả: SUCCESS hoặc FAILED")
    evidence_summary: str = Field(..., description="Tóm tắt bằng chứng")
    lesson_learned: str = Field(..., description="Bài học chắt lọc rút ra")
    key_learnings: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)
