"""Domain models for Architecture Fitness and Traceability Graph."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, auto


class FitnessDimension(Enum):
    DEPENDENCY_DIRECTION = auto()
    LAYER_BOUNDARY = auto()
    DOMAIN_PURITY = auto()
    NAMING_CONVENTION = auto()
    SECURITY_GUARD = auto()
    GOVERNANCE_RULE = auto()


@dataclass(frozen=True, slots=True)
class KnowledgeGraphLink:
    business_goal_id: str
    capability_id: str
    adr_id: str
    rule_id: str
    commit_hash: str
    author_id: str  # Developer hoặc AI Agent ID
    incident_id: str | None = None


@dataclass(frozen=True, slots=True)
class FitnessEvaluationResult:
    dimension: FitnessDimension
    rule_id: str
    passed: bool
    score: float  # 0.0 -> 1.0
    evidence_details: str


@dataclass(slots=True)
class FitnessSuiteAggregate:
    suite_id: str
    graph_link: KnowledgeGraphLink
    evaluations: list[FitnessEvaluationResult] = field(default_factory=list)
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def add_evaluation(self, eval_result: FitnessEvaluationResult) -> None:
        self.evaluations.append(eval_result)

    @property
    def overall_fitness_score(self) -> float:
        if not self.evaluations:
            return 0.0
        total_score = sum(e.score for e in self.evaluations)
        return round(total_score / len(self.evaluations), 4)

    @property
    def has_critical_violations(self) -> bool:
        return any(not e.passed for e in self.evaluations)
