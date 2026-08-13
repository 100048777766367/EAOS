from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Self-Healing Loop Domain Models (Phase 2)."""


class TracebackAnalysis(BaseModel):
    """Value object representing error traceback analysis."""

    model_config = ConfigDict(frozen=True)

    failed_stage: str = Field(..., description="Stage e.g. LINT, TEST")
    error_type: str = Field(..., description="Error classification")
    summary: str = Field(..., description="Error message summary")
    suggested_fix: str = Field(..., description="Fix recommendation")


class HealingCycleResult(BaseModel):
    """Result aggregate of a self-healing iteration."""

    model_config = ConfigDict(frozen=True)

    cycle_id: str = Field(..., description="Cycle ID")
    iterations: int = Field(default=1, description="Number of attempts")
    healed: bool = Field(default=True, description="Self-healing status")
    analysis: TracebackAnalysis | None = Field(default=None)
