from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from apps.api.bootstrap.container import prometheus_exporter

"""Prometheus Metrics scraping router."""


router = APIRouter(tags=["Telemetry"])


@router.get("/metrics", response_class=PlainTextResponse)
def metrics() -> str:
    exporter_fn = getattr(prometheus_exporter, "generate_prometheus_metrics_text", lambda: "")
    res: Any = exporter_fn()
    return str(res)
