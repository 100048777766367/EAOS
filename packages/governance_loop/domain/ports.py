"""Domain ports for Governance Loop context."""

from typing import Protocol

from packages.governance_loop.domain.models import (
    GovernanceCycleAggregate,
    InvariantCheck,
)


class GovernanceRepositoryPort(Protocol):
    def save(self, cycle: GovernanceCycleAggregate) -> None:
        ...

    def find_by_id(self, cycle_id: str) -> GovernanceCycleAggregate | None:
        ...


class PolicyEvaluatorPort(Protocol):
    def evaluate_invariants(self, target_ref: str) -> list[InvariantCheck]:
        ...


class AuditLedgerPort(Protocol):
    def commit_entry(self, cycle: GovernanceCycleAggregate) -> str:
        ...
