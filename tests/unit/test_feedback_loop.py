"""Unit tests for the Feedback Loop bounded context."""

from packages.feedback.application.dto import (
    IngestionSignalCommand,
)
from packages.feedback.application.use_cases import (
    ProcessFeedbackUseCase,
)
from packages.feedback.domain.models import (
    FeedbackLoopAggregate,
    FeedbackSeverity,
    FeedbackSignal,
    FeedbackSource,
)
from packages.feedback.infrastructure.adapters import (
    InMemoryFeedbackRepository,
    MockAdaptationHandler,
)


def test_feedback_signal_violation_detection() -> None:
    signal = FeedbackSignal(
        signal_id="SIG-001",
        source=FeedbackSource.FITNESS_FUNCTION,
        severity=FeedbackSeverity.ERROR,
        metric_name="architecture_score",
        observed_value=75.0,
        threshold_value=80.0,
        message="Architecture score below threshold",
    )
    assert signal.is_violation is True


def test_feedback_loop_cooldown_suppression() -> None:
    aggregate = FeedbackLoopAggregate(loop_id="LOOP-01", cooldown_seconds=60.0)
    signal = FeedbackSignal(
        signal_id="SIG-002",
        source=FeedbackSource.TELEMETRY,
        severity=FeedbackSeverity.ERROR,
        metric_name="latency_ms",
        observed_value=450.0,
        threshold_value=200.0,
        message="High latency detected",
    )

    decision1 = aggregate.evaluate_signal(signal, decision_id="DEC-1")
    assert decision1 is not None
    assert decision1.action_type == "SCALE_RESOURCES"

    decision2 = aggregate.evaluate_signal(signal, decision_id="DEC-2")
    assert decision2 is None


def test_process_feedback_use_case_execution() -> None:
    repo = InMemoryFeedbackRepository()
    handler = MockAdaptationHandler()
    use_case = ProcessFeedbackUseCase(repository=repo, adaptation_handler=handler)

    cmd = IngestionSignalCommand(
        signal_id="SIG-100",
        loop_id="LOOP-MAIN",
        source=FeedbackSource.FITNESS_FUNCTION,
        severity=FeedbackSeverity.ERROR,
        metric_name="layer_violation_count",
        observed_value=3.0,
        threshold_value=0.0,
        message="3 layer boundary violations detected",
    )

    result = use_case.execute(cmd)

    assert result.is_violation is True
    assert result.adaptation_triggered is True
    assert result.action_type == "TRIGGER_SELF_HEAL"
    assert result.requires_approval is False

    assert len(handler.handled_decisions) == 1
    assert handler.handled_decisions[0].parameters["observed"] == 3.0
