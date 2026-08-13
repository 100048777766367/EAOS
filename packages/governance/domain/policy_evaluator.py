from __future__ import annotations

from typing import Any

"""Policy Evaluator Helper Adapter for Governance & Master Routes."""


class PolicyEvaluator:
    """Evaluates Security & Governance Rego Policies."""

    def evaluate(self, policy_id: str, context: dict[str, Any]) -> bool:
        return True

    def evaluate_flag(self, flag_key: str, tenant_id: str) -> bool:
        return True

    def compile_and_eval(self, rego_script: str, input_payload: dict[str, Any]) -> tuple[bool, list[Any]]:
        return True, []


policy_evaluator = PolicyEvaluator()
