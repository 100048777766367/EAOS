"""Infrastructure adapters for Continuous Improvement context."""

from packages.continuous_improvement.domain.models import (
    ImprovementInitiativeAggregate,
)
from packages.continuous_improvement.domain.ports import (
    ImprovementRepositoryPort,
)


class InMemoryImprovementRepository(ImprovementRepositoryPort):
    def __init__(self) -> None:
        self._store: dict[str, ImprovementInitiativeAggregate] = {}

    def save(self, initiative: ImprovementInitiativeAggregate) -> None:
        self._store[initiative.initiative_id] = initiative

    def find_by_id(
        self, initiative_id: str
    ) -> ImprovementInitiativeAggregate | None:
        return self._store.get(initiative_id)

    def list_all(self) -> list[ImprovementInitiativeAggregate]:
        return list(self._store.values())
