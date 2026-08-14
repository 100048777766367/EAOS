"""DXS Self Healing domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path


class HealingStatus(StrEnum):
    PLANNED = "PLANNED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class HealingAction(StrEnum):
    """Supported healing operations."""

    REPAIR = "REPAIR"
    RESTART = "RESTART"
    ROLLBACK = "ROLLBACK"
    REBUILD = "REBUILD"


@dataclass
class HealingPlan:
    """Evidence-backed repair plan."""

    action: HealingAction
    target: str
    reason: str = ""
    evidence_hash: str | None = None
    status: HealingStatus = HealingStatus.PLANNED
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class HealingResult:
    """Healing execution result."""

    success: bool
    message: str
    evidence_hash: str | None = None
    action: HealingAction | None = None
    status: str = "HEALED"
    evidence: Path | None = None

    @property
    def hash(self) -> str | None:
        """Backward compatible evidence hash accessor."""

        return self.evidence_hash


__all__ = [
    "HealingAction",
    "HealingPlan",
    "HealingResult",
    "HealingStatus",
]
