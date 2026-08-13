from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class HealthStatus(StrEnum):
    """Repository health classification."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass(frozen=True)
class HealthReport:
    """Aggregate health result."""

    status: HealthStatus
    passed: int
    failed: int

    @property
    def healthy(self) -> bool:
        """Return whether health is fully healthy."""
        return self.status is HealthStatus.HEALTHY
