from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class TelemetryDatapoint(BaseModel):
    """Chỉ số đo lường hiệu năng thời gian thực từ container/kernel."""

    metric_name: str
    value: float
    unit: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class LiveTelemetryDaemon:
    """Daemon thu thập chỉ số sống và phát hiện nguy cơ quá tải."""

    def __init__(
        self,
        latency_threshold_ms: float = 500.0,
        error_rate_threshold: float = 0.01,
    ) -> None:
        self.latency_threshold_ms = latency_threshold_ms
        self.error_rate_threshold = error_rate_threshold
        self.datapoints: list[TelemetryDatapoint] = []

    def ingest_metric(self, metric_name: str, value: float, unit: str) -> bool:
        """Nạp chỉ số đo lường từ OpenTelemetry / Prometheus Collector."""
        dp = TelemetryDatapoint(metric_name=metric_name, value=value, unit=unit)
        self.datapoints.append(dp)
        return self._check_degradation(dp)

    def _check_degradation(self, dp: TelemetryDatapoint) -> bool:
        """Trả về trực tiếp kết quả đánh giá logic mảng Boolean."""
        is_latency_degraded = "latency" in dp.metric_name.lower() and dp.value > self.latency_threshold_ms
        is_error_degraded = "error_rate" in dp.metric_name.lower() and dp.value > self.error_rate_threshold
        return is_latency_degraded or is_error_degraded
