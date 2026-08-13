"""Agent Task orchestration."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

from agents.task.evidence.evidence_writer import EvidenceWriter
from agents.task.execution.task_executor import AgentTaskExecutor
from agents.task.models.task_models import (
    AgentTask,
    TaskResult,
    TaskState,
)
from agents.task.patch.patch_service import PatchService


class AgentTaskOrchestrator:
    """Coordinate planning, execution, patching, and evidence."""

    def __init__(
        self,
        project_root: Path,
        *,
        allow_mutation: bool = False,
    ) -> None:
        self.project_root = project_root.resolve()
        self.executor = AgentTaskExecutor(
            allow_mutation=allow_mutation,
        )
        self.patch_service = PatchService(
            allow_apply=allow_mutation,
        )
        self.evidence = EvidenceWriter(
            self.project_root,
        )

    async def execute(
        self,
        task: AgentTask,
    ) -> AsyncIterator[dict[str, object]]:
        """Execute one Agent Task and emit lifecycle events."""

        async for event in self.executor.execute(
            task,
            self.project_root,
        ):
            yield event

        task.transition(TaskState.VERIFYING)

        yield {
            "type": "task_lifecycle",
            "state": task.state.value,
            "task_id": task.task_id,
        }

        patch_id = self.patch_service.create_patch(
            self.project_root,
            task,
        )

        task.transition(TaskState.COMPLETED)

        result = TaskResult(
            task_id=task.task_id,
            state=task.state,
            success=True,
            message="Agent task execution completed.",
            patch_id=patch_id,
        )

        evidence_id = self.evidence.write(
            task,
            result,
        )

        yield {
            "type": "task_completed",
            "task_id": task.task_id,
            "patch_id": patch_id,
            "evidence_id": evidence_id,
            "state": task.state.value,
        }
