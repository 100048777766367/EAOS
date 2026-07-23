"""Planner AI Agent worker for task DAG decomposition."""

import time

from pydantic import BaseModel, ConfigDict


class PlanTaskDTO(BaseModel):
    """Value object representing a planned execution task."""

    model_config = ConfigDict(frozen=True)

    task_id: str
    description: str
    priority: str


class PlannerOutput(BaseModel):
    """Value object for planner task decomposition output."""

    model_config = ConfigDict(frozen=True)

    plan_id: str
    tasks: list[PlanTaskDTO]
    created_at: str


class PlannerAgentWorker:
    """AI Agent decomposing high-level business goals into tasks."""

    def decompose_goal(
        self,
        goal_description: str,
    ) -> PlannerOutput:
        """Transforms business goal into structured task queue."""
        tasks = [
            PlanTaskDTO(
                task_id="TASK-01",
                description=f"Analyze: {goal_description[:30]}",
                priority="P1",
            ),
            PlanTaskDTO(
                task_id="TASK-02",
                description="Implement Hexagonal Architecture Adapters",
                priority="P1",
            ),
        ]
        return PlannerOutput(
            plan_id=f"plan_{int(time.time())}",
            tasks=tasks,
            created_at="2026-07-23T14:41:00Z",
        )
