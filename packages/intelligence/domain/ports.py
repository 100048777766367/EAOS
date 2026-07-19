from typing import Protocol

from packages.intelligence.domain.models import (
    EcosystemPlan,
    OptimizationGoal,
    SemanticDecision,
)


class IntelligenceRegistryPort(Protocol):
    """Port định nghĩa hành vi lưu trữ và lập kế hoạch nhận thức."""

    def save_decision(self, decision: SemanticDecision) -> SemanticDecision: ...

    def find_decision_by_id(self, dec_id: str) -> SemanticDecision | None: ...

    def save_plan(self, plan: EcosystemPlan) -> EcosystemPlan: ...

    def find_plan_by_id(self, plan_id: str) -> EcosystemPlan | None: ...

    def save_optimization(self, goal: OptimizationGoal) -> OptimizationGoal: ...

    def list_optimizations(self) -> list[OptimizationGoal]: ...