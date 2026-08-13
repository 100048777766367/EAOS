"""Domain models for EAOS agent task execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class TaskState(StrEnum):
    """Lifecycle states for an agent task."""

    CREATED = "CREATED"
    PLANNED = "PLANNED"
    ASSIGNED = "ASSIGNED"
    EXECUTING = "EXECUTING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass(slots=True)
class AgentTask:
    """Mutable in-memory task aggregate."""

    request: str
    agent_id: str = "coder"
    task_id: str = field(default_factory=lambda: f"tsk-{uuid4().hex[:8]}")
    state: TaskState = TaskState.CREATED
    plan: list[str] = field(default_factory=list)
    result: str | None = None
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def transition(self, state: TaskState) -> None:
        """Move the task to a new lifecycle state."""
        self.state = state
        self.updated_at = datetime.now(UTC)

    def as_dict(self) -> dict[str, object]:
        """Serialize the task for events and evidence."""
        return {
            "task_id": self.task_id,
            "request": self.request,
            "agent_id": self.agent_id,
            "state": self.state.value,
            "plan": list(self.plan),
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
