"""Application service for agent task lifecycle."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

from .execution.executor import TaskExecutor
from .models import AgentTask, TaskState
from .planning.planner import TaskPlanner


class TaskManager:
    """Own task creation, planning, execution, and lifecycle state."""

    def __init__(self) -> None:
        """Initialize task execution services."""
        self.planner = TaskPlanner()
        self.executor = TaskExecutor()

    def create(
        self,
        request: str,
        agent_id: str = "coder",
    ) -> AgentTask:
        """Create a task aggregate."""
        if not request.strip():
            raise ValueError("Task request cannot be empty.")

        return AgentTask(
            request=request,
            agent_id=agent_id,
        )

    async def run(
        self,
        task: AgentTask,
        project_root: Path,
    ) -> AsyncIterator[dict[str, object]]:
        """Run the controlled task lifecycle."""
        yield {
            "type": "task_created",
            "task_id": task.task_id,
            "state": task.state.value,
        }

        self.planner.plan(task)
        task.transition(TaskState.PLANNED)

        yield {
            "type": "task_planned",
            "task_id": task.task_id,
            "state": task.state.value,
            "plan": list(task.plan),
        }

        task.transition(TaskState.ASSIGNED)

        yield {
            "type": "task_assigned",
            "task_id": task.task_id,
            "state": task.state.value,
            "agent_id": task.agent_id,
        }

        async for event in self.executor.execute(
            task,
            project_root,
        ):
            yield event

        task.transition(TaskState.VERIFYING)

        yield {
            "type": "task_verification_requested",
            "task_id": task.task_id,
            "state": task.state.value,
        }
