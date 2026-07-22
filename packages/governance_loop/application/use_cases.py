"""Application use cases for Governance Loop orchestration."""

from packages.governance_loop.application.dto import (
    GovernanceCycleResult,
    StartGovernanceCycleCommand,
)
from packages.governance_loop.domain.models import (
    CouncilVoteRecord,
    CycleStatus,
    GovernanceCycleAggregate,
)
from packages.governance_loop.domain.ports import (
    AuditLedgerPort,
    GovernanceRepositoryPort,
    PolicyEvaluatorPort,
)


class ExecuteGovernanceCycleUseCase:
    """Orchestrates invariant evaluation, voting, and ledger commitment."""

    def __init__(
        self,
        repository: GovernanceRepositoryPort,
        evaluator: PolicyEvaluatorPort,
        ledger: AuditLedgerPort,
    ) -> None:
        self._repository = repository
        self._evaluator = evaluator
        self._ledger = ledger

    def execute(self, command: StartGovernanceCycleCommand) -> GovernanceCycleResult:
        cycle = GovernanceCycleAggregate(
            cycle_id=command.cycle_id,
            cadence=command.cadence,
            target_ref=command.target_ref,
        )

        # 1. Run automated invariant checks
        checks = self._evaluator.evaluate_invariants(command.target_ref)
        for check in checks:
            cycle.add_check_result(check)

        # 2. Register council votes
        for voter_data in command.voters:
            cycle.add_vote(
                CouncilVoteRecord(
                    voter=voter_data["voter"],
                    decision=voter_data["decision"],
                    reason=voter_data.get("reason", "No reason provided"),
                )
            )

        # 3. Finalize cycle status
        final_status = cycle.evaluate_and_finalize()
        self._repository.save(cycle)

        # 4. Commit to immutable audit ledger if committed
        ledger_tx_hash: str | None = None
        if final_status == CycleStatus.COMMITTED:
            ledger_tx_hash = self._ledger.commit_entry(cycle)

        passed_count = sum(1 for c in cycle.checks if c.passed)
        failed_count = len(cycle.checks) - passed_count

        return GovernanceCycleResult(
            cycle_id=cycle.cycle_id,
            cadence=cycle.cadence.name,
            status=final_status.name,
            passed_checks_count=passed_count,
            failed_checks_count=failed_count,
            ledger_tx_hash=ledger_tx_hash,
        )
