"""Unit tests for the Governance Loop bounded context."""

from pathlib import Path

from packages.governance_loop.application.dto import StartGovernanceCycleCommand
from packages.governance_loop.application.use_cases import ExecuteGovernanceCycleUseCase
from packages.governance_loop.domain.models import (
    CycleStatus,
    GovernanceCycleAggregate,
    InvariantCheck,
    LoopCadence,
)
from packages.governance_loop.infrastructure.adapters import (
    FileAuditLedgerAdapter,
    InMemoryGovernanceRepository,
    StaticPolicyEvaluatorAdapter,
)


def test_governance_aggregate_commit_on_passing_checks() -> None:
    cycle = GovernanceCycleAggregate(
        cycle_id="CYC-001",
        cadence=LoopCadence.MEDIUM_ARCHITECTURE,
        target_ref="REF-ADR-006",
    )
    cycle.add_check_result(
        InvariantCheck(
            rule_id="R1",
            rule_name="Purpose First",
            passed=True,
            evidence="Valid business purpose mapped.",
        )
    )
    status = cycle.evaluate_and_finalize()
    assert status == CycleStatus.COMMITTED


def test_governance_aggregate_rejection_on_failing_check() -> None:
    cycle = GovernanceCycleAggregate(
        cycle_id="CYC-002",
        cadence=LoopCadence.FAST_EXECUTION,
        target_ref="COMMIT-FAIL-01",
    )
    cycle.add_check_result(
        InvariantCheck(
            rule_id="R4",
            rule_name="Stable Core",
            passed=False,
            evidence="Illegal import of infrastructure in domain layer.",
        )
    )
    status = cycle.evaluate_and_finalize()
    assert status == CycleStatus.REJECTED


def test_execute_governance_cycle_use_case_success(tmp_path: Path) -> None:
    repo = InMemoryGovernanceRepository()
    evaluator = StaticPolicyEvaluatorAdapter(simulate_failure=False)
    ledger_file = tmp_path / "audit_ledger.jsonl"
    ledger = FileAuditLedgerAdapter(ledger_file)

    use_case = ExecuteGovernanceCycleUseCase(
        repository=repo, evaluator=evaluator, ledger=ledger
    )

    cmd = StartGovernanceCycleCommand(
        cycle_id="CYC-100",
        cadence=LoopCadence.MEDIUM_ARCHITECTURE,
        target_ref="PR-1002-SPLAY",
        voters=[
            {"voter": "ArchitectAgent", "decision": "APPROVED", "reason": "OK"},
            {"voter": "ReviewerAgent", "decision": "APPROVED", "reason": "Pass"},
        ],
    )

    result = use_case.execute(cmd)

    assert result.status == "COMMITTED"
    assert result.passed_checks_count == 2
    assert result.failed_checks_count == 0
    assert result.ledger_tx_hash is not None
    assert ledger_file.exists()
