from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class LoopCycle(BaseModel):
    """Báº£n ghi mÃ´ táº£ chi tiáº¿t má»™t chu ká»³ tiáº¿n hÃ³a vÃ´ háº¡n Ä‘Ã³ng kÃ­n."""

    cycle_id: str = Field(..., description="MÃ£ chu ká»³")
    status: str = Field(..., description="Tráº¡ng thÃ¡i (SUCCESS/FAILED)")
    stage_executions: dict[str, str] = Field(default_factory=dict, description="Báº£n Ä‘á»“ liÃªn káº¿t tráº¡ng thÃ¡i")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class AutonomousLoopState(BaseModel):
    """MÃ´ hÃ¬nh biá»ƒu diá»…n tráº¡ng thÃ¡i cá»§a nhÃ¢n tiáº¿n hÃ³a tá»± trá»‹."""

    is_running: bool = Field(default=False)
    current_cycle_id: str | None = Field(default=None)
    last_run_at: datetime | None = Field(default=None)

    model_config = ConfigDict(frozen=True)
