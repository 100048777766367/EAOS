"""AI Pre-Commit Guard verifying code before AI Agents write to disk."""

import ast

from pydantic import BaseModel, ConfigDict


class GuardEvaluationDTO(BaseModel):
    """Value object representing pre-commit guard evaluation."""

    model_config = ConfigDict(frozen=True)

    passed: bool
    violations: list[str]
    risk_score: float


class AIPreCommitGuard:
    """Guard inspecting AI-generated Python code before disk commit."""

    FORBIDDEN_DOMAIN_IMPORTS: set[str] = {
        "fastapi",
        "sqlalchemy",
        "openai",
        "httpx",
    }

    def evaluate_code_patch(
        self,
        file_path: str,
        code_contents: str,
    ) -> GuardEvaluationDTO:
        """Evaluates proposed AST code patch against Constitution rules."""
        violations: list[str] = []
        if "domain" in file_path:
            try:
                tree = ast.parse(code_contents)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            mod = alias.name.split(".")[0]
                            if mod in self.FORBIDDEN_DOMAIN_IMPORTS:
                                violations.append(f"Forbidden import '{mod}' in domain")
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        mod = node.module.split(".")[0]
                        if mod in self.FORBIDDEN_DOMAIN_IMPORTS:
                            violations.append(f"Forbidden import '{mod}' in domain")
            except SyntaxError as e:
                violations.append(f"Syntax Error in generated patch: {e}")

        passed = len(violations) == 0
        risk = 0.0 if passed else 100.0
        return GuardEvaluationDTO(
            passed=passed,
            violations=violations,
            risk_score=risk,
        )


if __name__ == "__main__":
    guard = AIPreCommitGuard()
    sample = "import fastapi\nclass Test: pass"
    res = guard.evaluate_code_patch("packages/domain/models.py", sample)
    print(f"✔ AI Guard Self-Test Passed: {not res.passed}")
