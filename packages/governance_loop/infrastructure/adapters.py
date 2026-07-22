"""Infrastructure adapters for Governance Loop."""

import hashlib
import json
from pathlib import Path

from packages.governance_loop.domain.models import (
    GovernanceCycleAggregate,
    InvariantCheck,
)
from packages.governance_loop.domain.ports import (
    AuditLedgerPort,
    GovernanceRepositoryPort,
    PolicyEvaluatorPort,
)


class InMemoryGovernanceRepository(GovernanceRepositoryPort):
    def __init__(self) -> None:
        self._store: dict[str, GovernanceCycleAggregate] = {}

    def save(self, cycle: GovernanceCycleAggregate) -> None:
        self._store[cycle.cycle_id] = cycle

    def find_by_id(self, cycle_id: str) -> GovernanceCycleAggregate | None:
        return self._store.get(cycle_id)


class StaticPolicyEvaluatorAdapter(PolicyEvaluatorPort):
    def __init__(self, simulate_failure: bool = False) -> None:
        self._simulate_failure = simulate_failure

    def evaluate_invariants(self, target_ref: str) -> list[InvariantCheck]:
        return [
            InvariantCheck(
                rule_id="R4",
                rule_name="Stable Core Dependency Rule",
                passed=not self._simulate_failure,
                evidence=f"Checked target {target_ref} against AST imports.",
            ),
            InvariantCheck(
                rule_id="R15",
                rule_name="Rules Over Prompts",
                passed=True,
                evidence="Verified deterministic validation layers exist.",
            ),
        ]


class FileAuditLedgerAdapter(AuditLedgerPort):
    def __init__(self, ledger_file: Path) -> None:
        self._ledger_file = ledger_file
        self._ledger_file.parent.mkdir(parents=True, exist_ok=True)

    def commit_entry(self, cycle: GovernanceCycleAggregate) -> str:
        payload = {
            "cycle_id": cycle.cycle_id,
            "cadence": cycle.cadence.name,
            "target_ref": cycle.target_ref,
            "status": cycle.status.name,
            "checks_passed": len([c for c in cycle.checks if c.passed]),
        }

        serialized = json.dumps(payload, sort_keys=True)
        tx_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        payload["tx_hash"] = tx_hash

        with open(self._ledger_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")

        return tx_hash
