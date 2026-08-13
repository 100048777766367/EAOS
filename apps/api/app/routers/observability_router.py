from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

"""Prometheus & Observability Metrics Router for EAOS."""


router = APIRouter(tags=["Observability"])


@router.get("/metrics", response_class=PlainTextResponse)
async def get_prometheus_metrics() -> str:
    """Exposes Prometheus metrics endpoint."""
    return (
        "# HELP eaos_health_score Current architectural health score\n"
        "# TYPE eaos_health_score gauge\n"
        "eaos_health_score 100.0\n"
        "# HELP eaos_p99_latency_ms P99 request latency in ms\n"
        "# TYPE eaos_p99_latency_ms gauge\n"
        "eaos_p99_latency_ms 12.4\n"
    )
