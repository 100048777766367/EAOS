"""Unit tests for Prometheus Metrics Exporter Adapter."""

from packages.metrics_engine.application.dto import (
    ArchitectureHealthDashboardDTO,
    CapabilityHealthDTO,
)
from packages.metrics_engine.infrastructure.adapters import (
    PrometheusMetricsExporterAdapter,
)


def test_prometheus_metrics_exporter_format() -> None:
    dashboard = ArchitectureHealthDashboardDTO(
        system_id="EAOS-PROD-01",
        overall_health_score=92.50,
        mttr_minutes=18.50,
        ai_success_rate_percentage=98.00,
        architecture_drift_index=0.0250,
        capability_health_list=[
            CapabilityHealthDTO(
                capability_id="cap.knowledge",
                health_score=95.0,
                active_violations=0,
                active_incidents=0,
                drift_index=0.01,
                status="HEALTHY",
            ),
            CapabilityHealthDTO(
                capability_id="cap.identity",
                health_score=75.0,
                active_violations=2,
                active_incidents=1,
                drift_index=0.12,
                status="DEGRADED",
            ),
        ],
        computed_at="2026-07-22T12:00:00Z",
    )

    exporter = PrometheusMetricsExporterAdapter()
    output = exporter.export_prometheus_format(dashboard)

    # Verify Prometheus exposition standards
    assert "# HELP eaos_architecture_health_score" in output
    assert "# TYPE eaos_architecture_health_score gauge" in output
    assert 'eaos_architecture_health_score{system_id="EAOS-PROD-01"} 92.50' in output

    assert "# HELP eaos_architecture_mttr_minutes" in output
    assert 'eaos_architecture_mttr_minutes{system_id="EAOS-PROD-01"} 18.50' in output

    assert 'eaos_ai_success_rate_percentage{system_id="EAOS-PROD-01"} 98.00' in output
    assert 'eaos_architecture_drift_index{system_id="EAOS-PROD-01"} 0.0250' in output

    # Verify capability labels
    assert (
        'eaos_capability_health_score{capability_id="cap.knowledge",status="HEALTHY"} 95.00'
        in output
    )
    assert (
        'eaos_capability_health_score{capability_id="cap.identity",status="DEGRADED"} 75.00'
        in output
    )
    assert 'eaos_capability_active_violations{capability_id="cap.identity"} 2' in output
