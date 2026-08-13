from __future__ import annotations

from datetime import UTC, datetime

from dxs.observability.model import Observation


class ObservabilityService:
    """Collects deterministic DXS runtime observations."""

    def observe(
        self,
        name: str,
        value: float,
        unit: str = "",
    ) -> Observation:
        return Observation(
            name=name,
            timestamp=datetime.now(UTC),
            value=value,
            unit=unit,
        )


__all__ = ["ObservabilityService"]