"""Dynamic Architectural Fitness Function DSL compiler for EAOS."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class FitnessEvaluation(BaseModel):
    """Value object representing the result of a fitness evaluation."""

    model_config = ConfigDict(frozen=True)

    function_name: str
    passed: bool
    score: float
    violation_details: str


class DynamicFitnessCompiler:
    """Compiles and evaluates string DSL architectural fitness functions."""

    def compile_and_run(
        self,
        expression: str,
        metrics_context: dict[str, Any],
    ) -> FitnessEvaluation:
        """Evaluates DSL expression safely against metrics context."""
        try:
            passed = self._eval_expression(expression, metrics_context)
            score = 100.0 if passed else 0.0
            details = "Fitness condition satisfied." if passed else f"Violation detected for expression: '{expression}'"
        except Exception as exc:
            passed = False
            score = 0.0
            details = f"Compilation/Evaluation error: {exc!s}"

        fn_hash = hash(expression) & 0xFFFFFFFF
        return FitnessEvaluation(
            function_name=f"fitness_fn_{fn_hash:08x}",
            passed=passed,
            score=score,
            violation_details=details,
        )

    def _eval_expression(
        self,
        expression: str,
        context: dict[str, Any],
    ) -> bool:
        """Helper to parse comparison operators safely."""
        operators = [">=", "<=", "==", "!=", ">", "<"]
        matched_op = None
        for op in operators:
            if op in expression:
                matched_op = op
                break

        if not matched_op:
            return True

        parts = expression.split(matched_op)
        var_name = parts[0].strip()
        raw_val = parts[1].strip()

        actual_val = context.get(var_name)
        if actual_val is None:
            return False

        try:
            target_num = float(raw_val)
            actual_num = float(actual_val)
            if matched_op == ">=":
                return actual_num >= target_num
            if matched_op == "<=":
                return actual_num <= target_num
            if matched_op == ">":
                return actual_num > target_num
            if matched_op == "<":
                return actual_num < target_num
            if matched_op == "==":
                return actual_num == target_num
            if matched_op == "!=":
                return actual_num != target_num
        except ValueError:
            target_str = raw_val.strip('"').strip("'")
            actual_str = str(actual_val)
            if matched_op == "==":
                return actual_str == target_str
            if matched_op == "!=":
                return actual_str != target_str

        return True
