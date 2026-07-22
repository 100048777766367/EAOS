"""Infrastructure adapters for feedback persistence and handling."""


from packages.feedback.domain.models import (
    AdaptationDecision,
    FeedbackLoopAggregate,
    FeedbackSignal,
)
from packages.feedback.domain.ports import (
    AdaptationHandlerPort,
    FeedbackRepositoryPort,
)


class InMemoryFeedbackRepository(FeedbackRepositoryPort):
    """In-memory implementation for testing and local execution."""

    def __init__(self) -> None:
        self.signals: dict[str, FeedbackSignal] = {}
        self.decisions: dict[str, AdaptationDecision] = {}
        self.aggregates: dict[str, FeedbackLoopAggregate] = {}

    def save_signal(self, signal: FeedbackSignal) -> None:
        self.signals[signal.signal_id] = signal

    def save_decision(self, decision: AdaptationDecision) -> None:
        self.decisions[decision.decision_id] = decision

    def get_aggregate(
        self, loop_id: str
    ) -> FeedbackLoopAggregate | None:
        return self.aggregates.get(loop_id)

    def save_aggregate(
        self, aggregate: FeedbackLoopAggregate
    ) -> None:
        self.aggregates[aggregate.loop_id] = aggregate


class MockAdaptationHandler(AdaptationHandlerPort):
    """Mock implementation for testing adaptation dispatching."""

    def __init__(self) -> None:
        self.handled_decisions: list[AdaptationDecision] = []

    def handle_adaptation(
        self, decision: AdaptationDecision
    ) -> bool:
        self.handled_decisions.append(decision)
        return True
