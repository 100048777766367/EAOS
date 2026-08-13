from __future__ import annotations

from .model import HealthReport, HealthStatus


class HealthService:
    """Build deterministic health reports."""

    def evaluate(
        self,
        passed: int,
        failed: int,
    ) -> HealthReport:
        """Classify health from diagnostic counts."""
        if failed == 0:
            status = HealthStatus.HEALTHY
        elif passed > 0:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        return HealthReport(
            status=status,
            passed=passed,
            failed=failed,
        )
