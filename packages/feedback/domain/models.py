"""Domain models for the Feedback Loop bounded context."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, auto


class FeedbackSource(Enum):
    AGENT = auto()
    TELEMETRY = auto()
    FITNESS_FUNCTION = auto()
    GOVERNANCE_COUNCIL = auto()


class FeedbackSeverity(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


@dataclass(frozen=True, slots=True)
class FeedbackSignal:
    signal_id: str
    source: FeedbackSource
    severity: FeedbackSeverity
    metric_name: str
    observed_value: float
    threshold_value: float
    message: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    @property
    def is_violation(self) -> bool:
        if self.severity in (
            FeedbackSeverity.ERROR,
            FeedbackSeverity.CRITICAL,
        ):
            return True
        return self.observed_value > self.threshold_value


@dataclass(frozen=True, slots=True)
class AdaptationDecision:
    decision_id: str
    signal_id: str
    action_type: str
    parameters: dict[str, str | float | int | bool]
    requires_approval: bool
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )


@dataclass(slots=True)
class FeedbackLoopAggregate:
    loop_id: str
    cooldown_seconds: float = 60.0
    last_adaptation_at: datetime | None = None

    def evaluate_signal(
        self, signal: FeedbackSignal, decision_id: str
    ) -> AdaptationDecision | None:
        """Evaluates signal and determines adaptation requirement."""
        if not signal.is_violation:
            return None

        now = datetime.now(UTC)
        if self.last_adaptation_at is not None:
            elapsed = (
                now - self.last_adaptation_at
            ).total_seconds()
            if elapsed < self.cooldown_seconds:
                return None

        action_type = self._determine_action(signal)
        requires_approval = (
            signal.severity == FeedbackSeverity.CRITICAL
        )

        self.last_adaptation_at = now
        return AdaptationDecision(
            decision_id=decision_id,
            signal_id=signal.signal_id,
            action_type=action_type,
            parameters={
                "metric": signal.metric_name,
                "observed": signal.observed_value,
                "threshold": signal.threshold_value,
            },
            requires_approval=requires_approval,
            created_at=now,
        )

    def _determine_action(self, signal: FeedbackSignal) -> str:
        match signal.source:
            case FeedbackSource.FITNESS_FUNCTION:
                return "TRIGGER_SELF_HEAL"
            case FeedbackSource.TELEMETRY:
                return "SCALE_RESOURCES"
            case FeedbackSource.AGENT:
                return "ADJUST_PROMPT_TEMPERATURE"
            case FeedbackSource.GOVERNANCE_COUNCIL:
                return "REVERT_MIGRATION"

