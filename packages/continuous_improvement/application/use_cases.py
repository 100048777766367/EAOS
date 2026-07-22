"""Use cases for Continuous Improvement (Kaizen) engine."""

import uuid

from packages.continuous_improvement.application.dto import (
    IdentifyOpportunitiesCommand,
    ImprovementInitiativeDTO,
    VerifyInitiativeCommand,
)
from packages.continuous_improvement.domain.models import (
    ActionItem,
    ImprovementCategory,
    ImprovementInitiativeAggregate,
    MetricDelta,
)
from packages.continuous_improvement.domain.ports import (
    ImprovementRepositoryPort,
)


class IdentifyImprovementOpportunitiesUseCase:
    """Analyzes component health signals and creates prioritized Kaizen initiatives."""

    def __init__(self, repository: ImprovementRepositoryPort) -> None:
        self._repository = repository

    def execute(
        self, command: IdentifyOpportunitiesCommand
    ) -> ImprovementInitiativeDTO | None:
        # Trigger Rule 1: High Architecture Drift -> Decouple Boundaries
        if command.drift_index > 0.15:
            init_id = f"KAIZEN-{uuid.uuid4().hex[:6].upper()}"
            initiative = ImprovementInitiativeAggregate(
                initiative_id=init_id,
                title=f"Decouple Architecture Boundaries for {command.target_component}",
                category=ImprovementCategory.DECOUPLE_BOUNDARIES,
                target_component=command.target_component,
                metric_delta=MetricDelta(
                    metric_name="drift_index",
                    baseline_value=command.drift_index,
                    target_value=0.05,
                ),
                action_items=[
                    ActionItem(
                        item_id="ACT-01",
                        target_component=command.target_component,
                        description="Extract leaked infrastructure imports into Ports.",
                        estimated_risk_score=0.2,
                    )
                ],
            )
            self._repository.save(initiative)
            return self._map_to_dto(initiative)

        # Trigger Rule 2: Low Health Score -> Refactor Code
        if command.health_score < 80.0:
            init_id = f"KAIZEN-{uuid.uuid4().hex[:6].upper()}"
            initiative = ImprovementInitiativeAggregate(
                initiative_id=init_id,
                title=f"Refactor Domain Code for {command.target_component}",
                category=ImprovementCategory.REFACTOR_CODE,
                target_component=command.target_component,
                metric_delta=MetricDelta(
                    metric_name="health_score",
                    baseline_value=command.health_score,
                    target_value=95.0,
                ),
                action_items=[
                    ActionItem(
                        item_id="ACT-02",
                        target_component=command.target_component,
                        description="Eliminate rule violations and add unit tests.",
                        estimated_risk_score=0.1,
                    )
                ],
            )
            self._repository.save(initiative)
            return self._map_to_dto(initiative)

        return None

    def _map_to_dto(
        self, initiative: ImprovementInitiativeAggregate
    ) -> ImprovementInitiativeDTO:
        return ImprovementInitiativeDTO(
            initiative_id=initiative.initiative_id,
            title=initiative.title,
            category=initiative.category,
            target_component=initiative.target_component,
            roi_score=initiative.calculate_roi_score(),
            status=initiative.status,
            baseline_value=initiative.metric_delta.baseline_value,
            target_value=initiative.metric_delta.target_value,
            achieved_value=initiative.metric_delta.achieved_value,
        )


class VerifyInitiativeEffectivenessUseCase:
    """Verifies if an executed initiative truly improved the system metrics."""

    def __init__(self, repository: ImprovementRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: VerifyInitiativeCommand) -> bool:
        initiative = self._repository.find_by_id(command.initiative_id)
        if initiative is None:
            raise ValueError(f"Initiative {command.initiative_id} not found.")

        success = initiative.verify_effectiveness(command.current_metric_value)
        self._repository.save(initiative)
        return success
