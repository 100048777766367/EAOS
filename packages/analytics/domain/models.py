from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Analytics & Telemetry Domain Model for EAOS Capability App."""


class AnalyticsTrendPoint(BaseModel):
    """Value object representing a metric trend data point."""

    model_config = ConfigDict(frozen=True)

    value: float


class BusinessKPISnapshot(BaseModel):
    """Value object representing executive business health metrics."""

    model_config = ConfigDict(frozen=True)

    snapshot_id: str = Field(default="SNAP-001", description="Unique Snapshot ID")
    system_id: str = Field(default="SYS-001", description="System identifier")
    monthly_traffic: int = Field(default=0)
    conversion_rate: float = Field(default=0.0)
    net_revenue_usd: float = Field(default=0.0)
    roi_percentage: float = Field(default=0.0)
    trends: list[AnalyticsTrendPoint] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @property
    def metric_id(self) -> str:
        """Alias for metric ID compatibility."""
        return self.snapshot_id


# Alias for legacy infrastructure adapters compatibility
AnalyticsMetricEntity = BusinessKPISnapshot
