from typing import Any

from packages.metrics_engine.domain.models import ArchitectureHealthAggregate
from packages.metrics_engine.domain.ports import MetricsRepositoryPort


class InMemoryMetricsRepository(MetricsRepositoryPort):
    def __init__(self) -> None:
        self._store: dict[str, ArchitectureHealthAggregate] = {}

    def save(self, aggregate: ArchitectureHealthAggregate) -> None:
        self._store[aggregate.system_id] = aggregate

    def find_by_system_id(
        self, system_id: str
    ) -> ArchitectureHealthAggregate | None:
        return self._store.get(system_id)


class PrometheusMetricsExporterAdapter:
    """Formats ArchitectureHealthDashboardDTO into Prometheus text format."""

    def export_prometheus_format(self, dashboard_data: Any) -> str:
        system_id = getattr(dashboard_data, "system_id", "EAOS-CORE")
        overall_score = getattr(dashboard_data, "overall_health_score", 0.0)
        mttr = getattr(dashboard_data, "mttr_minutes", 0.0)
        ai_success = getattr(
            dashboard_data, "ai_success_rate_percentage", 0.0
        )
        drift_index = getattr(dashboard_data, "architecture_drift_index", 0.0)
        cap_list = getattr(dashboard_data, "capability_health_list", [])

        lines: list[str] = [
            "# HELP eaos_architecture_health_score Overall health score.",
            "# TYPE eaos_architecture_health_score gauge",
            f'eaos_architecture_health_score{{system_id="{system_id}"}} {overall_score:.2f}',
            "",
            "# HELP eaos_architecture_mttr_minutes Mean Time To Recovery.",
            "# TYPE eaos_architecture_mttr_minutes gauge",
            f'eaos_architecture_mttr_minutes{{system_id="{system_id}"}} {mttr:.2f}',
            "",
            "# HELP eaos_ai_success_rate_percentage AI success rate.",
            "# TYPE eaos_ai_success_rate_percentage gauge",
            f'eaos_ai_success_rate_percentage{{system_id="{system_id}"}} {ai_success:.2f}',
            "",
            "# HELP eaos_architecture_drift_index Architecture drift index.",
            "# TYPE eaos_architecture_drift_index gauge",
            f'eaos_architecture_drift_index{{system_id="{system_id}"}} {drift_index:.4f}',
            "",
        ]

        if cap_list:
            lines.extend([
                "# HELP eaos_capability_health_score Capability health score.",
                "# TYPE eaos_capability_health_score gauge",
            ])
            for cap in cap_list:
                cap_id = getattr(cap, "capability_id", "unknown")
                c_score = getattr(cap, "health_score", 0.0)
                status = getattr(cap, "status", "UNKNOWN")
                lines.append(
                    f'eaos_capability_health_score{{capability_id="{cap_id}",status="{status}"}} {c_score:.2f}'
                )
            lines.append("")

        return "\n".join(lines) + "\n"
