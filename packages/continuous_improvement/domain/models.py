"""Domain models for Continuous Improvement context."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, auto


class ImprovementCategory(Enum):
    REFACTOR_CODE = auto()
    DECOUPLE_BOUNDARIES = auto()
    OPTIMIZE_LATENCY = auto()
    UPDATE_POLICY = auto()
    ADJUST_AGENT_PROMPT = auto()


class InitiativeStatus(Enum):
    IDENTIFIED = auto()
    PROPOSED = auto()
    EXECUTING = auto()
    VERIFIED = auto()
    ROLLED_BACK = auto()


@dataclass(frozen=True, slots=True)
class MetricDelta:
    metric_name: str
    baseline_value: float
    target_value: float
    achieved_value: float | None = None

    @property
    def is_improved(self) -> bool:
        if self.achieved_value is None:
            return False
        # Higher is better for health/success rates, lower is better for latency/drift
        if "latency" in self.metric_name.lower() or "drift" in self.metric_name.lower():
            return self.achieved_value < self.baseline_value
        return self.achieved_value > self.baseline_value


@dataclass(frozen=True, slots=True)
class ActionItem:
    item_id: str
    target_component: str
    description: str
    estimated_risk_score: float  # 0.0 (Safe) -> 1.0 (High Risk)


@dataclass(slots=True)
class ImprovementInitiativeAggregate:
    initiative_id: str
    title: str
    category: ImprovementCategory
    target_component: str
    metric_delta: MetricDelta
    action_items: list[ActionItem] = field(default_factory=list)
    status: InitiativeStatus = InitiativeStatus.IDENTIFIED
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def calculate_roi_score(self) -> float:
        """Calculates Expected ROI = Expected Improvement / Total Risk Weight."""
        expected_gain = abs(self.metric_delta.target_value - self.metric_delta.baseline_value)
        total_risk = sum(item.estimated_risk_score for item in self.action_items) or 1.0
        return round(expected_gain / total_risk, 2)

    def mark_as_proposed(self) -> None:
        self.status = InitiativeStatus.PROPOSED

    def mark_as_executing(self) -> None:
        self.status = InitiativeStatus.EXECUTING

    def verify_effectiveness(self, current_metric_value: float) -> bool:
        """Verifies if post-execution metric achieved real improvement."""
        self.metric_delta = MetricDelta(
            metric_name=self.metric_delta.metric_name,
            baseline_value=self.metric_delta.baseline_value,
            target_value=self.metric_delta.target_value,
            achieved_value=current_metric_value,
        )

        if self.metric_delta.is_improved:
            self.status = InitiativeStatus.VERIFIED
            return True

        self.status = InitiativeStatus.ROLLED_BACK
        return False
