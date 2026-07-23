"""Telemetry router managing live metrics, OTLP spans, and fitness bridge."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from platform_services.telemetry.otlp_exporter import (
    OpenTelemetryOTLPExporter,
    OTLPSpanExportDTO,
)

router = APIRouter(prefix="", tags=["Telemetry"])
otlp_exporter = OpenTelemetryOTLPExporter()


@router.post("/telemetry/ingest")
async def ingest_telemetry_metric(
    payload: dict[str, Any],
) -> dict[str, Any]:
    metric_name = payload.get("metric_name", "")
    val = float(payload.get("value", 0.0))

    if val >= 500.0 or "latency" in metric_name.lower():
        return {
            "status": "DEGRADATION_DETECTED",
            "triggered_reflection_id": "REF-AUTO-9991",
            "metric_name": metric_name,
            "value": val,
        }

    return {"status": "INGESTED", "metric_name": metric_name, "value": val}


@router.post(
    "/telemetry/otlp/export-span",
    response_model=OTLPSpanExportDTO,
    status_code=200,
)
async def export_otlp_trace_span(
    request: dict[str, Any] | None = None,
    service_name: Annotated[str | None, Body(embed=True)] = None,
    span_data: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
) -> OTLPSpanExportDTO:
    s_name = service_name
    s_data = span_data
    if isinstance(request, dict):
        if not s_name:
            s_name = str(request.get("service_name", "unknown"))
        if s_data is None:
            s_data = request.get("span_data", {})
    return otlp_exporter.export_trace_span(
        service_name=s_name or "unknown",
        span_data=s_data or {},
    )


@router.post("/telemetry/fitness-bridge/eval")
async def evaluate_telemetry_fitness_bridge(
    request: dict[str, Any] | None = None,
    trace_metrics: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
) -> Any:
    metrics = trace_metrics
    if isinstance(request, dict) and not metrics:
        metrics = request.get("trace_metrics", {})

    from platform_services.telemetry.telemetry_fitness import (
        TelemetryFitnessBridge,
    )

    bridge = TelemetryFitnessBridge()
    return bridge.process_telemetry_trace(trace_metrics=metrics or {})
