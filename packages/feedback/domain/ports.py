"""Domain ports for the Feedback Loop bounded context."""

from typing import Protocol

from packages.feedback.domain.models import (
    AdaptationDecision,
    FeedbackLoopAggregate,
    FeedbackSignal,
)


class FeedbackRepositoryPort(Protocol):
    """Port for persisting feedback signals and decisions."""

    def save_signal(self, signal: FeedbackSignal) -> None:
        ...

    def save_decision(self, decision: AdaptationDecision) -> None:
        ...

    def get_aggregate(
        self, loop_id: str
    ) -> FeedbackLoopAggregate | None:
        ...

    def save_aggregate(
        self, aggregate: FeedbackLoopAggregate
    ) -> None:
        ...


class AdaptationHandlerPort(Protocol):
    """Port for dispatching adaptation actions."""

    def handle_adaptation(
        self, decision: AdaptationDecision
    ) -> bool:
        ...
