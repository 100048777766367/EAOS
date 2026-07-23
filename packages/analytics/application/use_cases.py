"""Application use cases for Analytics bounded context."""

from packages.analytics.domain.models import (
    AnalyticsMetricEntity,
    MetricTrendVO,
)


class ComputeSystemHealthUseCase:
    """Use case computing system health score from telemetry trends."""

    def execute(
        self,
        system_id: str,
        metric_value: float,
    ) -> AnalyticsMetricEntity:
        """Processes telemetry input and generates health metric entity."""
        trend = MetricTrendVO(
            metric_name="p99_latency",
            value=metric_value,
            unit="ms",
        )
        return AnalyticsMetricEntity(
            metric_id=f"metric_{system_id}",
            system_id=system_id,
            trends=[trend],
        )
