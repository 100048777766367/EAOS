"""Application use cases for Feedback processing."""

import uuid

from packages.feedback.application.dto import (
    FeedbackProcessResult,
    IngestionSignalCommand,
)
from packages.feedback.domain.models import (
    FeedbackLoopAggregate,
    FeedbackSignal,
)
from packages.feedback.domain.ports import (
    AdaptationHandlerPort,
    FeedbackRepositoryPort,
)


class ProcessFeedbackUseCase:
    """Orchestrates feedback signal ingestion and adaptation."""

    def __init__(
        self,
        repository: FeedbackRepositoryPort,
        adaptation_handler: AdaptationHandlerPort,
    ) -> None:
        self._repository = repository
        self._adaptation_handler = adaptation_handler

    def execute(
        self, command: IngestionSignalCommand
    ) -> FeedbackProcessResult:
        signal = FeedbackSignal(
            signal_id=command.signal_id,
            source=command.source,
            severity=command.severity,
            metric_name=command.metric_name,
            observed_value=command.observed_value,
            threshold_value=command.threshold_value,
            message=command.message,
        )

        self._repository.save_signal(signal)

        aggregate = self._repository.get_aggregate(
            command.loop_id
        )
        if aggregate is None:
            aggregate = FeedbackLoopAggregate(
                loop_id=command.loop_id
            )

        decision_id = f"DEC-{uuid.uuid4().hex[:8].upper()}"
        decision = aggregate.evaluate_signal(
            signal, decision_id=decision_id
        )

        self._repository.save_aggregate(aggregate)

        if decision is None:
            return FeedbackProcessResult(
                signal_id=signal.signal_id,
                is_violation=signal.is_violation,
                adaptation_triggered=False,
            )

        self._repository.save_decision(decision)

        if not decision.requires_approval:
            self._adaptation_handler.handle_adaptation(decision)

        return FeedbackProcessResult(
            signal_id=signal.signal_id,
            is_violation=True,
            adaptation_triggered=True,
            decision_id=decision.decision_id,
            action_type=decision.action_type,
            requires_approval=decision.requires_approval,
        )
