"""Infrastructure storage adapters for Analytics bounded context."""

from typing import Any

from packages.analytics.domain.models import AnalyticsMetricEntity


class InMemoryAnalyticsRepository:
    """In-memory repository storing analytics metric entities."""

    def __init__(self) -> None:
        self._metrics: dict[str, AnalyticsMetricEntity] = {}

    def save(
        self,
        metric: AnalyticsMetricEntity,
    ) -> AnalyticsMetricEntity:
        """Saves metric entity in memory."""
        self._metrics[metric.metric_id] = metric
        return metric

    def find_by_system_id(
        self,
        system_id: str,
    ) -> Any | None:
        """Finds metric entity by system ID."""
        for item in self._metrics.values():
            if item.system_id == system_id:
                return item
        return None
