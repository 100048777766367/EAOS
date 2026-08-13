from typing import Any, Protocol

from packages.metrics_engine.domain.models import ArchitectureHealthAggregate

"""Domain ports for Enterprise Metrics Engine context."""


class MetricsRepositoryPort(Protocol):
    def save(self, aggregate: ArchitectureHealthAggregate) -> None: ...

    def find_by_system_id(self, system_id: str) -> ArchitectureHealthAggregate | None: ...


class MetricsExporterPort(Protocol):
    """Port for exporting architecture health metrics to external monitoring format."""

    def export_prometheus_format(self, dashboard_data: Any) -> str: ...
