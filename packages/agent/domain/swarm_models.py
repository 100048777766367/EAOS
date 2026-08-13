from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Multi-Agent Swarm Domain Models (Phase 4)."""


class AgentRole(StrEnum):
    """Roles in the 5-Agent Swarm Orchestration pipeline."""

    PLANNER = "PLANNER"
    ARCHITECT = "ARCHITECT"
    CODER = "CODER"
    REVIEWER = "REVIEWER"
    TESTER = "TESTER"


class AgentStepResult(BaseModel):
    """Result produced by an individual Swarm Agent."""

    model_config = ConfigDict(frozen=True)

    role: AgentRole = Field(..., description="Agent role")
    success: bool = Field(default=True, description="Step status")
    output_summary: str = Field(default="", description="Agent output")
    evidence_data: dict[str, Any] = Field(default_factory=dict)


class SwarmExecutionResult(BaseModel):
    """Aggregate result of 5-Agent Swarm execution."""

    model_config = ConfigDict(frozen=True)

    swarm_id: str = Field(..., description="Unique swarm execution ID")
    goal: str = Field(..., description="User goal description")
    success: bool = Field(default=True, description="Overall status")
    step_results: list[AgentStepResult] = Field(default_factory=list)
    completed_agents: int = Field(default=0, description="Completed count")
