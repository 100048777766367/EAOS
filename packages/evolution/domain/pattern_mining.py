from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Pattern Mining Engine Models (v4.x Autonomous Learning)."""


class CandidateRule(BaseModel):
    """Candidate rule synthesized from incident pattern mining."""

    model_config = ConfigDict(frozen=True)

    rule_id: str = Field(..., description="Candidate rule ID")
    statement: str = Field(..., description="Rule statement")
    source_incidents_count: int = Field(default=1)
    simulated_pass_rate: float = Field(default=1.0)
    approved: bool = Field(default=False)


class PatternMiningResult(BaseModel):
    """Result of mining patterns across enterprise memory."""

    model_config = ConfigDict(frozen=True)

    mined_patterns_count: int = Field(default=0)
    candidate_rules: list[CandidateRule] = Field(default_factory=list)
    recommended_adrs: list[str] = Field(default_factory=list)
