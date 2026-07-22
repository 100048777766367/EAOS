"""Application use cases for Enterprise Metrics Engine."""

from datetime import UTC, datetime

from packages.metrics_engine.application.dto import (
    ArchitectureHealthDashboardDTO,
    CapabilityHealthDTO,
    RecordObservationCommand,
)
from packages.metrics_engine.domain.models import (
    ArchitectureHealthAggregate,
    RawMetricObservation,
)
from packages.metrics_engine.domain.ports import MetricsRepositoryPort


class RecordMetricObservationUseCase:
    def __init__(self, repository: MetricsRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: RecordObservationCommand) -> None:
        aggregate = self._repository.find_by_system_id(command.system_id)
        if aggregate is None:
            aggregate = ArchitectureHealthAggregate(system_id=command.system_id)

        aggregate.add_observation(
            RawMetricObservation(
                observation_id=command.observation_id,
                metric_type=command.metric_type,
                value=command.value,
                target_component=command.target_component,
            )
        )

        self._repository.save(aggregate)


class ComputeArchitectureHealthUseCase:
    """Computes comprehensive health dashboard metrics for EAOS."""

    def __init__(self, repository: MetricsRepositoryPort) -> None:
        self._repository = repository

    def execute(self, system_id: str, capability_ids: list[str]) -> ArchitectureHealthDashboardDTO:
        aggregate = self._repository.find_by_system_id(system_id)
        if aggregate is None:
            aggregate = ArchitectureHealthAggregate(system_id=system_id)

        cap_reports = []
        for cap_id in capability_ids:
            score = aggregate.evaluate_capability_health(cap_id)
            cap_reports.append(
                CapabilityHealthDTO(
                    capability_id=score.capability_id,
                    health_score=score.health_score,
                    active_violations=score.active_violations,
                    active_incidents=score.active_incidents,
                    drift_index=score.drift_index,
                    status=score.status,
                )
            )

        return ArchitectureHealthDashboardDTO(
            system_id=aggregate.system_id,
            overall_health_score=aggregate.compute_overall_system_health(),
            mttr_minutes=aggregate.calculate_mttr(),
            ai_success_rate_percentage=aggregate.calculate_ai_success_rate(),
            architecture_drift_index=(aggregate.calculate_architecture_drift_index()),
            capability_health_list=cap_reports,
            computed_at=datetime.now(UTC).isoformat(),
        )
