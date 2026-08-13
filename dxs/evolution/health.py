from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class HealthStatus(StrEnum):
    """Normalized repository health status."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass(frozen=True)
class HealthCheck:
    """One deterministic repository health observation."""

    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class HealthModel:
    """Aggregate repository health model."""

    status: HealthStatus
    checks: tuple[HealthCheck, ...]

    @classmethod
    def from_checks(
        cls,
        checks: tuple[HealthCheck, ...],
    ) -> HealthModel:
        """Build health status from real checks."""
        if not checks:
            return cls(
                status=HealthStatus.DEGRADED,
                checks=checks,
            )

        passed = sum(check.passed for check in checks)

        if passed == len(checks):
            status = HealthStatus.HEALTHY
        elif passed == 0:
            status = HealthStatus.UNHEALTHY
        else:
            status = HealthStatus.DEGRADED

        return cls(status=status, checks=checks)
