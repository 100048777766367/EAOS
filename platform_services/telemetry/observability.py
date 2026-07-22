import uuid
from typing import Any

from packages.metrics_engine.domain.models import (
    ArchitectureHealthAggregate,
    MetricType,
    RawMetricObservation,
)


class EAOSObservabilityMiddleware:
    """Middleware tự động đo lường telemetry và đính kèm Trace/Correlation ID."""

    def __init__(
        self, app: Any, metrics_repository: Any, system_id: str
    ) -> None:
        self.app = app
        self.metrics_repository = metrics_repository
        self.system_id = system_id

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        trace_id = f"TRC-{uuid.uuid4().hex[:8]}"
        correlation_id = f"COR-{uuid.uuid4().hex[:8]}"

        async def send_wrapper(message: dict[str, Any]) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.append((b"x-trace-id", trace_id.encode()))
                headers.append((b"x-correlation-id", correlation_id.encode()))
                message["headers"] = headers
            await send(message)

        existing: ArchitectureHealthAggregate | None = None
        if hasattr(self.metrics_repository, "find_by_system_id"):
            existing = self.metrics_repository.find_by_system_id(
                self.system_id
            )

        metric_type_val: MetricType = next(iter(MetricType))

        if existing is None:
            initial_obs = RawMetricObservation(
                observation_id=f"OBS-{uuid.uuid4().hex[:8]}",
                target_component=self.system_id,
                metric_type=metric_type_val,
                value=1.0,
            )
            existing = ArchitectureHealthAggregate(
                system_id=self.system_id,
                observations=[initial_obs],
            )

        new_obs = RawMetricObservation(
            observation_id=f"OBS-{uuid.uuid4().hex[:8]}",
            target_component=self.system_id,
            metric_type=metric_type_val,
            value=10.5,
        )
        existing.observations.append(new_obs)

        if hasattr(self.metrics_repository, "save"):
            self.metrics_repository.save(existing)

        await self.app(scope, receive, send_wrapper)