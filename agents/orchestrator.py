"""Top-level agent task orchestration."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

from .task_execution.execution.executor import TaskExecutor
from .task_execution.models import AgentTask, TaskState
from .task_execution.task_manager import TaskManager


class AgentOrchestrator:
    """Coordinate task creation and governed execution."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()
        self.manager = TaskManager()
        self.executor = TaskExecutor()

    def create_task(
        self,
        goal: str,
        agent_id: str = "coder",
    ) -> AgentTask:
        """Create a task without executing it."""
        return self.manager.create(goal, agent_id)

    async def execute(
        self,
        task: AgentTask,
    ) -> AsyncIterator[dict[str, object]]:
        """Execute a task through the execution boundary."""
        yield {
            "type": "agent_task",
            "state": TaskState.CREATED.value,
            "task_id": task.task_id,
            "agent_id": task.agent_id,
        }

        async for event in self.executor.execute(
            task,
            self.project_root,
        ):
            yield event
