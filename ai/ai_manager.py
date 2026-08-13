from __future__ import annotations

from .automation.dry_run_ai_simulator import DryRunAiSimulator
from .evaluation.hallucination_guard import HallucinationGuard
from .planner.task_decomposer import AITaskDecomposer
from .router.model_router import FinOpsModelRouter

"""AI manager module."""


class AiManager:
    """Ai manager implementation."""

    def __init__(self) -> None:
        self.router = FinOpsModelRouter()
        self.decomposer = AITaskDecomposer()
        self.guard = HallucinationGuard()
        self.simulator = DryRunAiSimulator()
