"""Domain models for Agent Task execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


class TaskState(StrEnum):
    """Lifecycle states for an agent task."""

    CREATED = "CREATED"
    PLANNED = "PLANNED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RECOVERING = "RECOVERING"


@dataclass(slots=True)
class AgentTask:
    """Mutable runtime representation of an agent task."""

    request_id: str
    goal: str
    agent_id: str = "coder"
    task_id: str = field(
        default_factory=lambda: f"tsk-{uuid4().hex[:8]}",
    )
    state: TaskState = TaskState.CREATED
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def transition(self, state: TaskState) -> None:
        """Move the task to a new lifecycle state."""
        self.state = state


@dataclass(frozen=True, slots=True)
class TaskResult:
    """Result returned after task execution."""

    task_id: str
    state: TaskState
    success: bool
    message: str
    evidence_id: str | None = None
    patch_id: str | None = None
