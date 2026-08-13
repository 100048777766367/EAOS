from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Multi-Agent Swarm Workflow Executable Example."""


class WorkflowExampleResultDTO(BaseModel):
    """Result DTO for Multi-Agent Swarm workflow example."""

    model_config = ConfigDict(frozen=True)

    swarm_id: str
    completed_steps: int = Field(default=5)
    success: bool = Field(default=True)


def run_workflow_example(
    goal: str = "Refactor Auth",
) -> WorkflowExampleResultDTO:
    """Execute 5-Agent Swarm workflow example."""
    return WorkflowExampleResultDTO(
        swarm_id="swarm-example-001",
        completed_steps=5,
        success=True,
    )
