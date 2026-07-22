"""Domain ports for Continuous Improvement context."""

from typing import Protocol

from packages.continuous_improvement.domain.models import (
    ImprovementInitiativeAggregate,
)


class ImprovementRepositoryPort(Protocol):
    def save(self, initiative: ImprovementInitiativeAggregate) -> None: ...

    def find_by_id(self, initiative_id: str) -> ImprovementInitiativeAggregate | None: ...

    def list_all(self) -> list[ImprovementInitiativeAggregate]: ...


class MetricsCollectorSourcePort(Protocol):
    def get_current_metric(self, target_component: str, metric_name: str) -> float: ...
