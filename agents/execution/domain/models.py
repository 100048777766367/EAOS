"""Domain models for EAOS agent task execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any


class TaskState(StrEnum):
    """Task lifecycle states."""

    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    MUTATING = "MUTATING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class MutationState(StrEnum):
    """Mutation lifecycle states."""

    NONE = "NONE"
    PREPARED = "PREPARED"
    APPLIED = "APPLIED"
    REJECTED = "REJECTED"
    ROLLED_BACK = "ROLLED_BACK"


@dataclass(slots=True)
class TaskRequest:
    """Request to execute an agent task."""

    task_id: str
    user_request: str
    agent_id: str
    project_root: Path
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TaskResult:
    """Final task execution result."""

    task_id: str
    state: TaskState
    summary: str
    verification_status: str | None = None
    evidence_id: str | None = None
    mutation_state: MutationState = MutationState.NONE
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        """Serialize task result."""
        return {
            "task_id": self.task_id,
            "state": self.state.value,
            "summary": self.summary,
            "verification_status": self.verification_status,
            "evidence_id": self.evidence_id,
            "mutation_state": self.mutation_state.value,
            "error": self.error,
        }


@dataclass(slots=True)
class TaskEvent:
    """Runtime event emitted by the execution subsystem."""

    type: str
    task_id: str
    state: TaskState | None = None
    payload: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """Serialize event."""
        result: dict[str, Any] = {
            "type": self.type,
            "task_id": self.task_id,
            "payload": self.payload,
        }

        if self.state is not None:
            result["state"] = self.state.value

        return result
