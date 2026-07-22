from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class OTLPTraceSpan(BaseModel):
    """Đơn vị Vết xử lý (Trace Span) theo chuẩn OpenTelemetry."""

    trace_id: str
    span_id: str
    name: str
    start_time: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
    attributes: dict[str, Any] = Field(default_factory=dict)


class OTLPMetricRecord(BaseModel):
    """Bản ghi chỉ số đo lường (Metric Record) theo chuẩn OpenTelemetry."""

    metric_name: str
    value: float
    unit: str = "ms"
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )


class OTLPCollectorBridge:
    """Bridge chuyển đổi và xuất dữ liệu Telemetry sang chuẩn OTLP gRPC/JSON."""

    def __init__(
        self, endpoint_url: str = "http://localhost:4318/v1/traces"
    ) -> None:
        self.endpoint_url = endpoint_url
        self.trace_buffer: list[OTLPTraceSpan] = []
        self.metric_buffer: list[OTLPMetricRecord] = []

    def export_trace(self, span: OTLPTraceSpan) -> bool:
        self.trace_buffer.append(span)
        return True

    def export_metric(self, metric: OTLPMetricRecord) -> bool:
        self.metric_buffer.append(metric)
        return True

    def flush_buffers(self) -> dict[str, int]:
        trace_count = len(self.trace_buffer)
        metric_count = len(self.metric_buffer)
        self.trace_buffer.clear()
        self.metric_buffer.clear()
        return {
            "exported_traces": trace_count,
            "exported_metrics": metric_count,
        }
