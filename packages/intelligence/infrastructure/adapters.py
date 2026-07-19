from packages.intelligence.domain.models import (
    EcosystemPlan,
    OptimizationGoal,
    SemanticDecision,
)
from packages.intelligence.domain.ports import IntelligenceRegistryPort


class InMemoryIntelligenceRegistry(IntelligenceRegistryPort):
    """Adapter lưu trữ kết quả nhận thức trí tuệ tích hợp chỉ số hiệu năng."""

    def __init__(self) -> None:
        self._decisions: dict[str, SemanticDecision] = {}
        self._plans: dict[str, EcosystemPlan] = {}
        self._optimizations: list[OptimizationGoal] = []
        self._success_decisions_count: int = 0
        self._total_decisions_count: int = 0

    def save_decision(self, decision: SemanticDecision) -> SemanticDecision:
        self._decisions[decision.id] = decision
        self._total_decisions_count += 1
        if decision.confidence_score >= 0.90:
            self._success_decisions_count += 1
        return decision

    def find_decision_by_id(self, dec_id: str) -> SemanticDecision | None:
        return self._decisions.get(dec_id)

    def save_plan(self, plan: EcosystemPlan) -> EcosystemPlan:
        self._plans[plan.id] = plan
        return plan

    def find_plan_by_id(self, plan_id: str) -> EcosystemPlan | None:
        return self._plans.get(plan_id)

    def save_optimization(self, goal: OptimizationGoal) -> OptimizationGoal:
        self._optimizations.append(goal)
        return goal

    def list_optimizations(self) -> list[OptimizationGoal]:
        return self._optimizations

    def get_success_rate(self) -> float:
        """Đo đạc chỉ số (Metrics): Tỷ lệ các quyết định có độ tin cậy cao."""
        if self._total_decisions_count == 0:
            return 1.0
        return self._success_decisions_count / self._total_decisions_count
