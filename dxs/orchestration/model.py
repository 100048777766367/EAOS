from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ExecutionStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    name: str
    status: ExecutionStatus
    message: str = ""


__all__ = ["ExecutionResult", "ExecutionStatus"]