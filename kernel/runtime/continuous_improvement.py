"""Continuous Improvement Daemon executing the 18-stage DAG loop."""

import asyncio
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from packages.feedback.application.dto import IngestionSignalCommand
from packages.feedback.application.use_cases import ProcessFeedbackUseCase
from packages.feedback.domain.models import FeedbackSeverity, FeedbackSource
from packages.policy_engine.application.dto import EvaluatePolicyCommand
from packages.policy_engine.application.use_cases import EvaluatePolicyUseCase
from tools.metrics.architecture_metrics_calculator import (
    ArchitectureMetricsCalculator,
)


@dataclass(frozen=True, slots=True)
class ImprovementCycleRecord:
    cycle_id: str
    architecture_score: int
    policy_passed: bool
    adaptation_action: str | None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class ContinuousImprovementEngine:
    """Orchestrates the continuous improvement loop in the background."""

    def __init__(
        self,
        root_dir: Path,
        policy_use_case: EvaluatePolicyUseCase,
        feedback_use_case: ProcessFeedbackUseCase,
        interval_seconds: float = 300.0,
    ) -> None:
        self._root_dir = root_dir
        self._policy_use_case = policy_use_case
        self._feedback_use_case = feedback_use_case
        self._interval_seconds = interval_seconds
        self._history: list[ImprovementCycleRecord] = []
        self._is_running: bool = False

    async def start_daemon(self) -> None:
        """Starts the background continuous improvement daemon loop."""
        self._is_running = True
        while self._is_running:
            try:
                self.run_single_improvement_cycle()
            except Exception as err:
                print(f"[ContinuousImprovement] Error in cycle: {err}")
            await asyncio.sleep(self._interval_seconds)

    def stop_daemon(self) -> None:
        self._is_running = False

    def run_single_improvement_cycle(self) -> ImprovementCycleRecord:
        import uuid

        cycle_id = f"IMP-{uuid.uuid4().hex[:6].upper()}"

        # 1. Metrics Engine
        metrics_calc = ArchitectureMetricsCalculator(self._root_dir)
        metrics_calc.calculate_all()
        score = metrics_calc.architecture_score

        # 2. Policy Engine
        policy_cmd = EvaluatePolicyCommand(
            policy_id="POL-PROD-GUARD",
            context_payload={
                "metadata": {"environment": "production"},
                "payload": {"max_retry_loops": 5},
            },
        )
        policy_result = self._policy_use_case.execute(policy_cmd)

        # 3. Feedback Loop Evaluation
        action_triggered: str | None = None
        if score < 85 or not policy_result.is_allowed:
            signal_cmd = IngestionSignalCommand(
                signal_id=f"SIG-{cycle_id}",
                loop_id="LOOP-CONTINUOUS-IMPROVEMENT",
                source=FeedbackSource.FITNESS_FUNCTION,
                severity=FeedbackSeverity.ERROR,
                metric_name="architecture_score",
                observed_value=float(score),
                threshold_value=85.0,
                message="Architecture score below threshold",
            )
            feedback_res = self._feedback_use_case.execute(signal_cmd)
            action_triggered = feedback_res.action_type

        record = ImprovementCycleRecord(
            cycle_id=cycle_id,
            architecture_score=score,
            policy_passed=policy_result.is_allowed,
            adaptation_action=action_triggered,
        )
        self._history.append(record)
        return record

    @property
    def history(self) -> list[ImprovementCycleRecord]:
        return list(self._history)
