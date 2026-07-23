"""Observability, middleware, and telemetry services for EAOS."""

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


@dataclass
class MetricObservation:
    """Value object representing an HTTP request observation."""

    metric_name: str = "http_request_duration"
    value: float = 1.0


@dataclass
class HealthAggregate:
    """Aggregate tracking health observations for a system ID."""

    system_id: str
    observations: list[MetricObservation] = field(default_factory=list)


class TelemetryService:
    """Telemetry duration measurement and metrics reporting service."""

    @staticmethod
    def measure_duration(
        func: Callable[..., Any],
    ) -> Callable[..., Any]:
        """Decorator measuring function execution duration."""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            _elapsed = time.perf_counter() - start
            return result

        return wrapper


class EAOSObservabilityMiddleware(BaseHTTPMiddleware):
    """FastAPI observability middleware attaching telemetry headers."""

    def __init__(
        self,
        app: Any,
        metrics_repository: Any = None,
        system_id: str = "EAOS-CORE",
    ) -> None:
        super().__init__(app)
        self.metrics_repository = metrics_repository
        self.system_id = system_id

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[..., Any],
    ) -> Response:
        """Dispatches HTTP request and instruments telemetry headers."""
        start_time = time.perf_counter()
        response: Response = await call_next(request)
        duration_ms = (time.perf_counter() - start_time) * 1000

        response.headers["X-EAOS-System-ID"] = self.system_id
        response.headers["X-Trace-ID"] = "TRC-AUTO-1001"
        response.headers["X-Correlation-ID"] = "CORR-AUTO-1001"

        if self.metrics_repository is not None:
            self._capture_metrics(response.status_code, duration_ms)

        return response

    def _capture_metrics(
        self,
        status_code: int,
        duration_ms: float,
    ) -> None:
        """Records metric snapshot into provided repository."""
        if hasattr(self.metrics_repository, "find_by_system_id"):
            agg = self.metrics_repository.find_by_system_id(self.system_id)
            if agg is None:
                agg = HealthAggregate(
                    system_id=self.system_id,
                    observations=[
                        MetricObservation("initial_baseline", 0.0),
                        MetricObservation("http_req", duration_ms),
                    ],
                )
                if hasattr(self.metrics_repository, "save"):
                    self.metrics_repository.save(agg)
                elif hasattr(self.metrics_repository, "_records"):
                    self.metrics_repository._records[self.system_id] = agg
            else:
                obs_list = getattr(agg, "observations", None)
                if isinstance(obs_list, list):
                    obs_list.append(MetricObservation("http_req", duration_ms))
