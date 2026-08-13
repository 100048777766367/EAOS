"""Resource Lock Manager enforcing fine-grained concurrency control for multi-agent execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class ResourceLockDTO:
    """Immutable representation of an active resource lock."""

    resource_id: str  # e.g. "file:apps/api/app/main.py"
    holder_agent_id: str
    task_id: str
    acquired_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    reason: str = ""


class ResourceLockConflictError(RuntimeError):
    """Raised when an agent attempts to acquire a lock held by another agent."""


class ResourceLockManager:
    """Manages resource locks to prevent conflicting concurrent agent mutations."""

    def __init__(self) -> None:
        self._active_locks: dict[str, ResourceLockDTO] = {}

    def acquire_lock(self, resource_id: str, agent_id: str, task_id: str, reason: str = "") -> ResourceLockDTO:
        """Acquires a lock for a target resource or raises ResourceLockConflictError."""
        existing = self._active_locks.get(resource_id)
        if existing:
            if existing.holder_agent_id != agent_id or existing.task_id != task_id:
                raise ResourceLockConflictError(
                    f"Resource lock conflict on '{resource_id}': "
                    f"Already held by agent '{existing.holder_agent_id}' "
                    f"for task '{existing.task_id}'"
                )
            return existing

        lock = ResourceLockDTO(
            resource_id=resource_id,
            holder_agent_id=agent_id,
            task_id=task_id,
            reason=reason,
        )
        self._active_locks[resource_id] = lock
        return lock

    def release_lock(self, resource_id: str, agent_id: str, task_id: str) -> bool:
        """Releases lock if held by requesting agent and task."""
        existing = self._active_locks.get(resource_id)
        if existing and existing.holder_agent_id == agent_id and existing.task_id == task_id:
            del self._active_locks[resource_id]
            return True
        return False

    def release_all_for_task(self, task_id: str) -> int:
        """Releases all locks associated with a task ID."""
        to_remove = [r_id for r_id, lock_item in self._active_locks.items() if lock_item.task_id == task_id]
        for r_id in to_remove:
            del self._active_locks[r_id]
        return len(to_remove)

    def list_active_locks(self) -> list[ResourceLockDTO]:
        """Lists all active resource locks."""
        return list(self._active_locks.values())
