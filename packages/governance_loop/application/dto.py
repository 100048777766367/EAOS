"""Data Transfer Objects for Governance Loop application layer."""

from packages.governance_loop.domain.models import LoopCadence
from pydantic import BaseModel, Field


class StartGovernanceCycleCommand(BaseModel):
    cycle_id: str = Field(..., description="Unique ID for the governance cycle")
    cadence: LoopCadence
    target_ref: str = Field(..., description="Target commit, ADR, or spec ref")
    voters: list[dict[str, str]] = Field(default_factory=list)


class GovernanceCycleResult(BaseModel):
    cycle_id: str
    cadence: str
    status: str
    passed_checks_count: int
    failed_checks_count: int
    ledger_tx_hash: str | None = None
