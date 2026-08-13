"""Task Lifecycle Finite State Machine (FSM) for EAOS Runtime Control Plane."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class TaskState(StrEnum):
    """Canonical Task States in EAOS Runtime Control Plane."""

    CREATED = "CREATED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"
    RECOVERING = "RECOVERING"


# Allowed transitions map
VALID_TRANSITIONS: dict[TaskState, set[TaskState]] = {
    TaskState.CREATED: {TaskState.QUEUED, TaskState.CANCELLED, TaskState.BLOCKED},
    TaskState.QUEUED: {TaskState.RUNNING, TaskState.CANCELLED, TaskState.BLOCKED},
    TaskState.RUNNING: {TaskState.VERIFYING, TaskState.FAILED, TaskState.CANCELLED, TaskState.BLOCKED},
    TaskState.VERIFYING: {TaskState.COMPLETED, TaskState.FAILED, TaskState.RECOVERING, TaskState.BLOCKED},
    TaskState.RECOVERING: {TaskState.RUNNING, TaskState.VERIFYING, TaskState.FAILED, TaskState.BLOCKED},
    TaskState.FAILED: {TaskState.RECOVERING, TaskState.CANCELLED},
    TaskState.BLOCKED: {TaskState.QUEUED, TaskState.RUNNING, TaskState.CANCELLED},
    TaskState.COMPLETED: set(),
    TaskState.CANCELLED: set(),
}


@dataclass(frozen=True)
class StateTransitionEvent:
    """Immutable record of a task state transition with evidence."""

    task_id: str
    from_state: TaskState
    to_state: TaskState
    timestamp: str
    evidence_token: str
    metadata: dict[str, Any] = field(default_factory=dict)


class TaskLifecycleError(ValueError):
    """Raised when an invalid task lifecycle transition is attempted."""


class TaskLifecycleFSM:
    """Finite State Machine enforcing valid Task Lifecycle transitions."""

    def __init__(self, task_id: str, initial_state: TaskState = TaskState.CREATED) -> None:
        self.task_id = task_id
        self._current_state = initial_state
        self._history: list[StateTransitionEvent] = []
        # Record creation event
        self._record_transition(initial_state, initial_state, "INIT-TOKEN", {"reason": "Task created"})

    @property
    def current_state(self) -> TaskState:
        return self._current_state

    @property
    def history(self) -> list[StateTransitionEvent]:
        return list(self._history)

    def transition_to(
        self,
        target_state: TaskState,
        evidence_token: str,
        metadata: dict[str, Any] | None = None,
    ) -> StateTransitionEvent:
        """Transitions task state to target_state if valid under rules."""
        if target_state not in VALID_TRANSITIONS.get(self._current_state, set()):
            raise TaskLifecycleError(
                f"Invalid transition for task {self.task_id}: {self._current_state.value} -> {target_state.value}"
            )

        prev_state = self._current_state
        self._current_state = target_state
        return self._record_transition(prev_state, target_state, evidence_token, metadata or {})

    def _record_transition(
        self,
        from_state: TaskState,
        to_state: TaskState,
        evidence_token: str,
        metadata: dict[str, Any],
    ) -> StateTransitionEvent:
        event = StateTransitionEvent(
            task_id=self.task_id,
            from_state=from_state,
            to_state=to_state,
            timestamp=datetime.now(UTC).isoformat(),
            evidence_token=evidence_token,
            metadata=metadata,
        )
        self._history.append(event)
        return event
