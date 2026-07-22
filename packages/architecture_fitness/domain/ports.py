"""Domain ports for Architecture Fitness and Graph Traceability."""

from typing import Protocol

from packages.architecture_fitness.domain.models import (
    FitnessSuiteAggregate,
)


class FitnessRepositoryPort(Protocol):
    def save(self, suite: FitnessSuiteAggregate) -> None:
        ...

    def find_by_id(self, suite_id: str) -> FitnessSuiteAggregate | None:
        ...

    def list_all(self) -> list[FitnessSuiteAggregate]:
        ...


class GraphTraceabilityQueryPort(Protocol):
    def find_most_incident_prone_adrs(self) -> list[tuple[str, int]]:
        """Returns list of (adr_id, incident_count) sorted by incident impact."""
        ...
