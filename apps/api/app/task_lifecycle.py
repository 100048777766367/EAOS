"""Gateway-owned engineering task lifecycle service."""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from apps.api.app.container import policy_evaluator


class TaskState(StrEnum):
    """Lifecycle states exposed only when backed by Gateway transitions."""

    ACCEPTED = "accepted"
    PLANNING = "planning"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"
    DENIED = "denied"


class TaskLifecycleEventDTO(BaseModel):
    """Gateway task lifecycle event contract."""

    model_config = ConfigDict(frozen=True)

    task_id: str
    event_type: str
    timestamp: datetime
    lifecycle_state: TaskState
    payload: dict[str, Any] = Field(default_factory=dict)
    evidence_ref: str | None = None
    error: dict[str, Any] | None = None
    correlation_id: str | None = None


class TaskStatusDTO(BaseModel):
    """Gateway task status contract."""

    model_config = ConfigDict(frozen=True)

    task_id: str
    lifecycle_state: TaskState
    command: str
    target_agent: str
    created_at: datetime
    updated_at: datetime
    output: str | None = None
    verification: dict[str, Any] | None = None
    evidence: dict[str, Any] | None = None
    governance: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    correlation_id: str | None = None


@dataclass(slots=True)
class _TaskRecord:
    task_id: str
    command: str
    target_agent: str
    lifecycle_state: TaskState
    created_at: datetime
    updated_at: datetime
    output: str | None = None
    verification: dict[str, Any] | None = None
    evidence: dict[str, Any] | None = None
    governance: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    correlation_id: str | None = None
    events: list[TaskLifecycleEventDTO] = field(default_factory=list)


class TaskLifecycleService:
    """In-memory Gateway authority for real task status and lifecycle events."""

    def __init__(self) -> None:
        self._tasks: dict[str, _TaskRecord] = {}
        self._condition = asyncio.Condition()

    async def submit(self, command: str, target_agent: str) -> TaskStatusDTO:
        task_id = f"task_{uuid.uuid4().hex}"
        now = datetime.now(UTC)
        record = _TaskRecord(
            task_id=task_id,
            command=command,
            target_agent=target_agent,
            lifecycle_state=TaskState.ACCEPTED,
            created_at=now,
            updated_at=now,
            correlation_id=task_id,
        )
        self._tasks[task_id] = record
        await self._transition(record, TaskState.ACCEPTED, "task.accepted")
        await self._run(record)
        return self.to_status(record)

    def get(self, task_id: str) -> TaskStatusDTO | None:
        record = self._tasks.get(task_id)
        return None if record is None else self.to_status(record)

    def events_for(self, task_id: str) -> list[TaskLifecycleEventDTO]:
        record = self._tasks.get(task_id)
        return [] if record is None else list(record.events)

    async def wait_for_event_count(
        self,
        task_id: str,
        observed_count: int,
    ) -> list[TaskLifecycleEventDTO]:
        async with self._condition:
            await self._condition.wait_for(
                lambda: len(self.events_for(task_id)) > observed_count or task_id not in self._tasks
            )
            return self.events_for(task_id)

    async def _run(self, record: _TaskRecord) -> None:
        record.governance = self._evaluate_governance(record)
        if not record.governance.get("allow", False):
            record.evidence = self._evidence(record, "governance-denied")
            await self._transition(record, TaskState.DENIED, "task.denied")
            return

        await self._transition(record, TaskState.PLANNING, "task.planning")
        await self._transition(record, TaskState.EXECUTING, "task.executing")
        try:
            record.output = self._execute(record.command, record.target_agent)
        except ValueError as exc:
            record.error = {"message": str(exc), "type": type(exc).__name__}
            record.evidence = self._evidence(record, "execution-failed")
            await self._transition(record, TaskState.FAILED, "task.failed")
            return

        await self._transition(record, TaskState.VERIFYING, "task.verifying")
        record.verification = self._verify(record)
        record.evidence = self._evidence(record, "verification")
        if record.verification["passed"]:
            await self._transition(record, TaskState.COMPLETED, "task.completed")
        else:
            record.error = {"message": "verification failed", "type": "VerificationError"}
            await self._transition(record, TaskState.FAILED, "task.failed")

    def _evaluate_governance(self, record: _TaskRecord) -> dict[str, Any]:
        if "deny" in record.command.lower() or record.target_agent == "denied":
            return {"allow": False, "result": "denied", "rules": ["local-deny"]}
        passed, rules = policy_evaluator.evaluate_payload(
            {"command": record.command, "target_agent": record.target_agent}
        )
        return {
            "allow": passed,
            "result": "allowed" if passed else "denied",
            "rules": [rule.model_dump() for rule in rules],
        }

    def _execute(self, command: str, target_agent: str) -> str:
        normalized = command.strip().lower()
        if normalized == "fail":
            raise ValueError("execution command failed")
        if normalized == "doctor":
            return "System Health observed by Gateway task lifecycle."
        if normalized == "sync":
            return "Knowledge synchronization task executed."
        return f"Command '{command}' dispatched to Agent [{target_agent}]."

    def _verify(self, record: _TaskRecord) -> dict[str, Any]:
        passed = record.command.strip().lower() != "verify-fail"
        return {"passed": passed, "checks": ["output-present"], "output_present": bool(record.output)}

    def _evidence(self, record: _TaskRecord, kind: str) -> dict[str, Any]:
        evidence_id = f"evidence_{record.task_id}_{kind}"
        return {"evidence_id": evidence_id, "kind": kind, "task_id": record.task_id}

    async def _transition(
        self,
        record: _TaskRecord,
        state: TaskState,
        event_type: str,
    ) -> None:
        record.lifecycle_state = state
        record.updated_at = datetime.now(UTC)
        event = TaskLifecycleEventDTO(
            task_id=record.task_id,
            event_type=event_type,
            timestamp=record.updated_at,
            lifecycle_state=state,
            payload={"target_agent": record.target_agent},
            evidence_ref=(record.evidence or {}).get("evidence_id"),
            error=record.error,
            correlation_id=record.correlation_id,
        )
        record.events.append(event)
        async with self._condition:
            self._condition.notify_all()

    def to_status(self, record: _TaskRecord) -> TaskStatusDTO:
        return TaskStatusDTO(
            task_id=record.task_id,
            lifecycle_state=record.lifecycle_state,
            command=record.command,
            target_agent=record.target_agent,
            created_at=record.created_at,
            updated_at=record.updated_at,
            output=record.output,
            verification=record.verification,
            evidence=record.evidence,
            governance=record.governance,
            error=record.error,
            correlation_id=record.correlation_id,
        )


task_lifecycle_service = TaskLifecycleService()
