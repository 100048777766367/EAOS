"""Domain models for Governance Loop bounded context."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, auto


class LoopCadence(Enum):
    FAST_EXECUTION = auto()
    MEDIUM_ARCHITECTURE = auto()
    SLOW_STRATEGY = auto()


class CycleStatus(Enum):
    INITIATED = auto()
    EVALUATING = auto()
    COMMITTED = auto()
    REJECTED = auto()


@dataclass(frozen=True, slots=True)
class InvariantCheck:
    rule_id: str
    rule_name: str
    passed: bool
    evidence: str
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class CouncilVoteRecord:
    voter: str
    decision: str  # "APPROVED" | "REJECTED"
    reason: str


@dataclass(slots=True)
class GovernanceCycleAggregate:
    cycle_id: str
    cadence: LoopCadence
    target_ref: str
    status: CycleStatus = CycleStatus.INITIATED
    checks: list[InvariantCheck] = field(default_factory=list)
    votes: list[CouncilVoteRecord] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def add_check_result(self, check: InvariantCheck) -> None:
        if self.status != CycleStatus.INITIATED and self.status != CycleStatus.EVALUATING:
            raise ValueError("Cannot add checks to a finalized cycle.")
        self.status = CycleStatus.EVALUATING
        self.checks.append(check)

    def add_vote(self, vote: CouncilVoteRecord) -> None:
        self.votes.append(vote)

    def evaluate_and_finalize(self) -> CycleStatus:
        """Determines if the cycle is COMMITTED or REJECTED based on invariants and votes."""
        all_checks_passed = all(c.passed for c in self.checks) if self.checks else True

        approved_votes = sum(1 for v in self.votes if v.decision == "APPROVED")
        majority_voted = approved_votes >= (len(self.votes) / 2) if self.votes else True

        if all_checks_passed and majority_voted:
            self.status = CycleStatus.COMMITTED
        else:
            self.status = CycleStatus.REJECTED

        return self.status
