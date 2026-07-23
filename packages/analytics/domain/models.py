"""Domain entities and value objects for Analytics bounded context."""

from pydantic import BaseModel, ConfigDict


class MetricTrendVO(BaseModel):
    """Value object representing a metric trend snapshot."""

    model_config = ConfigDict(frozen=True)

    metric_name: str
    value: float
    unit: str


class AnalyticsMetricEntity(BaseModel):
    """Entity representing an aggregated architecture metric."""

    metric_id: str
    system_id: str
    trends: list[MetricTrendVO]
