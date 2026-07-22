"""Adapters for Fitness storage and Graph Traceability analysis."""

from collections import Counter

from packages.architecture_fitness.domain.models import (
    FitnessSuiteAggregate,
)
from packages.architecture_fitness.domain.ports import (
    FitnessRepositoryPort,
    GraphTraceabilityQueryPort,
)


class InMemoryFitnessRepository(
    FitnessRepositoryPort, GraphTraceabilityQueryPort
):
    def __init__(self) -> None:
        self._store: dict[str, FitnessSuiteAggregate] = {}

    def save(self, suite: FitnessSuiteAggregate) -> None:
        self._store[suite.suite_id] = suite

    def find_by_id(self, suite_id: str) -> FitnessSuiteAggregate | None:
        return self._store.get(suite_id)

    def list_all(self) -> list[FitnessSuiteAggregate]:
        return list(self._store.values())

    def find_most_incident_prone_adrs(self) -> list[tuple[str, int]]:
        """Walks knowledge graph links to count incidents associated with ADRs."""
        adr_counter: Counter[str] = Counter()

        for suite in self._store.values():
            link = suite.graph_link
            if link.incident_id is not None:
                adr_counter[link.adr_id] += 1

        return adr_counter.most_common()
