"""Unit tests for Enterprise Metrics Engine context."""

from packages.metrics_engine.application.dto import RecordObservationCommand
from packages.metrics_engine.application.use_cases import (
    ComputeArchitectureHealthUseCase,
    RecordMetricObservationUseCase,
)
from packages.metrics_engine.domain.models import MetricType
from packages.metrics_engine.infrastructure.adapters import (
    InMemoryMetricsRepository,
)


def test_metrics_engine_observation_and_health_computation() -> None:
    repo = InMemoryMetricsRepository()
    record_uc = RecordMetricObservationUseCase(repo)
    compute_uc = ComputeArchitectureHealthUseCase(repo)

    # 1. Record MTTR observations (Resolution times in minutes)
    record_uc.execute(
        RecordObservationCommand(
            observation_id="OBS-01",
            metric_type=MetricType.MTTR_MINUTES,
            value=15.0,
            target_component="SYSTEM",
        )
    )
    record_uc.execute(
        RecordObservationCommand(
            observation_id="OBS-02",
            metric_type=MetricType.MTTR_MINUTES,
            value=25.0,
            target_component="SYSTEM",
        )
    )

    # 2. Record AI Agent Success Rate (1 = success, 0 = failure)
    record_uc.execute(
        RecordObservationCommand(
            observation_id="OBS-03",
            metric_type=MetricType.AI_SUCCESS_RATE,
            value=1.0,
            target_component="agent.coder",
        )
    )
    record_uc.execute(
        RecordObservationCommand(
            observation_id="OBS-04",
            metric_type=MetricType.AI_SUCCESS_RATE,
            value=1.0,
            target_component="agent.coder",
        )
    )

    # 3. Record Capability-specific Rule Violations & Drift Index
    record_uc.execute(
        RecordObservationCommand(
            observation_id="OBS-05",
            metric_type=MetricType.RULE_VIOLATION_COUNT,
            value=1.0,
            target_component="cap.knowledge",
        )
    )
    record_uc.execute(
        RecordObservationCommand(
            observation_id="OBS-06",
            metric_type=MetricType.ARCHITECTURE_DRIFT_INDEX,
            value=0.15,
            target_component="cap.knowledge",
        )
    )

    # 4. Compute Health Dashboard
    dashboard = compute_uc.execute(
        system_id="EAOS-CORE",
        capability_ids=["cap.knowledge", "cap.identity"],
    )

    # Verify MTTR = Average(15, 25) = 20.0 minutes
    assert dashboard.mttr_minutes == 20.0
    assert dashboard.ai_success_rate_percentage == 100.0
    assert dashboard.architecture_drift_index == 0.15

    # Verify capability-specific health
    knowledge_cap = next(
        c
        for c in dashboard.capability_health_list
        if c.capability_id == "cap.knowledge"
    )
    # Penalty = (1 violation * 10) + (0 incidents * 15) + (0.15 drift * 30) = 10 + 4.5 = 14.5
    # Health Score = 100 - 14.5 = 85.5 -> HEALTHY
    assert knowledge_cap.health_score == 85.5
    assert knowledge_cap.status == "HEALTHY"

    identity_cap = next(
        c
        for c in dashboard.capability_health_list
        if c.capability_id == "cap.identity"
    )
    assert identity_cap.health_score == 100.0
    assert identity_cap.status == "HEALTHY"
