from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class LoopCycle(BaseModel):
    """Bản ghi mô tả chi tiết một chu kỳ tiến hóa vô hạn đóng kín."""

    cycle_id: str = Field(..., description="Mã chu kỳ")
    status: str = Field(..., description="Trạng thái (SUCCESS/FAILED)")
    stage_executions: dict[str, str] = Field(
        default_factory=dict, description="Bản đồ liên kết trạng thái"
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class AutonomousLoopState(BaseModel):
    """Mô hình biểu diễn trạng thái của nhân tiến hóa tự trị."""

    is_running: bool = Field(default=False)
    current_cycle_id: str | None = Field(default=None)
    last_run_at: datetime | None = Field(default=None)

    model_config = ConfigDict(frozen=True)