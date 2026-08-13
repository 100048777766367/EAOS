"""EAOS Agent Task Execution Engine."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

from ..domain.models import (
    MutationState,
    TaskEvent,
    TaskRequest,
    TaskResult,
    TaskState,
)
from ..evidence.evidence_store import ExecutionEvidenceStore
from ..mutation.repository_guard import RepositoryMutationGuard
from ..patch.patch_manager import PatchManager
from ..verification.eaos_verification_adapter import (
    EAOSVerificationAdapter,
)


class AgentTaskExecutionEngine:
    """Coordinate planning, execution, mutation, patching,
    verification, and evidence.
    """

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()
        self.guard = RepositoryMutationGuard()
        self.patch = PatchManager()
        self.evidence = ExecutionEvidenceStore(self.project_root)
        self.verification = EAOSVerificationAdapter(self.project_root)

    async def execute(
        self,
        request: TaskRequest,
    ) -> AsyncIterator[dict[str, Any]]:
        """Execute one governed task."""

        yield TaskEvent(
            type="task_execution_started",
            task_id=request.task_id,
            state=TaskState.QUEUED,
            payload={
                "agent_id": request.agent_id,
                "user_request": request.user_request,
            },
        ).as_dict()

        try:
            self.guard.prepare(self.project_root)

            yield TaskEvent(
                type="task_state",
                task_id=request.task_id,
                state=TaskState.PLANNING,
            ).as_dict()

            snapshot = self.guard.snapshot(self.project_root)

            yield TaskEvent(
                type="task_snapshot",
                task_id=request.task_id,
                state=TaskState.PLANNING,
                payload={
                    "revision": snapshot,
                },
            ).as_dict()

            yield TaskEvent(
                type="task_state",
                task_id=request.task_id,
                state=TaskState.EXECUTING,
            ).as_dict()

            yield TaskEvent(
                type="agent_execution_ready",
                task_id=request.task_id,
                state=TaskState.EXECUTING,
                payload={
                    "agent_id": request.agent_id,
                },
            ).as_dict()

            yield TaskEvent(
                type="task_state",
                task_id=request.task_id,
                state=TaskState.MUTATING,
            ).as_dict()

            mutation_state = self.guard.prepare(self.project_root)

            patch_before = self.patch.capture(self.project_root)

            yield TaskEvent(
                type="patch_snapshot",
                task_id=request.task_id,
                state=TaskState.MUTATING,
                payload={
                    "base_revision": (patch_before.base_revision),
                    "changed": patch_before.changed,
                },
            ).as_dict()

            yield TaskEvent(
                type="task_state",
                task_id=request.task_id,
                state=TaskState.VERIFYING,
            ).as_dict()

            verification = await self.verification.verify()

            verification_result = verification["result"]
            verification_status = verification_result["status"]

            patch_after = self.patch.capture(self.project_root)

            evidence_payload = {
                "task_id": request.task_id,
                "agent_id": request.agent_id,
                "request": request.user_request,
                "mutation_state": mutation_state.value,
                "verification": verification_result,
                "patch": {
                    "base_revision": (patch_after.base_revision),
                    "diff": patch_after.diff,
                },
            }

            evidence_id = self.evidence.store(evidence_payload)

            final_state = TaskState.COMPLETED if verification_status == "PASSED" else TaskState.FAILED

            result = TaskResult(
                task_id=request.task_id,
                state=final_state,
                summary=(
                    "Agent task verification passed."
                    if final_state == TaskState.COMPLETED
                    else "Agent task verification failed."
                ),
                verification_status=verification_status,
                evidence_id=evidence_id,
                mutation_state=MutationState.APPLIED,
            )

            yield TaskEvent(
                type="task_execution_result",
                task_id=request.task_id,
                state=final_state,
                payload=result.as_dict(),
            ).as_dict()

            return

        except Exception as exc:
            result = TaskResult(
                task_id=request.task_id,
                state=TaskState.FAILED,
                summary="Agent task execution failed.",
                mutation_state=MutationState.REJECTED,
                error=str(exc),
            )

            evidence_id = self.evidence.store(
                {
                    "task_id": request.task_id,
                    "agent_id": request.agent_id,
                    "error": str(exc),
                    "result": result.as_dict(),
                }
            )

            result.evidence_id = evidence_id

            yield TaskEvent(
                type="task_execution_result",
                task_id=request.task_id,
                state=TaskState.FAILED,
                payload=result.as_dict(),
            ).as_dict()
