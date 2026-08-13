from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class MigrationReadiness(StrEnum):
    """Migration readiness state."""

    READY = "ready"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class MigrationReadinessReport:
    """Deterministic migration readiness result."""

    status: MigrationReadiness
    reasons: tuple[str, ...]

    @property
    def ready(self) -> bool:
        """Return whether migration is ready."""
        return self.status is MigrationReadiness.READY


class MigrationReadinessService:
    """Evaluate whether migration prerequisites are satisfied."""

    def evaluate(
        self,
        compatibility_ok: bool,
        unresolved_findings: int,
    ) -> MigrationReadinessReport:
        """Evaluate migration prerequisites."""
        reasons: list[str] = []

        if not compatibility_ok:
            reasons.append("Compatibility check failed.")

        if unresolved_findings > 0:
            reasons.append("Unresolved diagnostic findings remain.")

        status = MigrationReadiness.READY if not reasons else MigrationReadiness.BLOCKED

        return MigrationReadinessReport(
            status=status,
            reasons=tuple(reasons),
        )
