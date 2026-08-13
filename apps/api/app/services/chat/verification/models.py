"""Domain models for EAOS verification."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class VerificationStatus(StrEnum):
    """Verification status."""

    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


@dataclass(frozen=True, slots=True)
class VerificationRun:
    """Result of one verification runner."""

    name: str
    status: VerificationStatus
    returncode: int | None = None
    output: str = ""
    duration_seconds: float = 0.0
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        """Serialize runner result."""
        return {
            "name": self.name,
            "status": self.status.value,
            "returncode": self.returncode,
            "output": self.output,
            "duration_seconds": self.duration_seconds,
            "error": self.error,
        }


@dataclass(frozen=True, slots=True)
class VerificationResult:
    """Aggregated verification result."""

    status: VerificationStatus
    runs: tuple[VerificationRun, ...] = field(
        default_factory=tuple,
    )
    evidence_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        """Serialize aggregate result."""
        return {
            "status": self.status.value,
            "runs": [run.as_dict() for run in self.runs],
            "evidence_id": self.evidence_id,
        }
