import ast

from pydantic import BaseModel, ConfigDict

"""Sprint 5 Engine: Rule Toolkit (RTK) for Executable Architecture Rules."""


class RuleCheckResultDTO(BaseModel):
    """Value object representing RTK rule check & fix proposal."""

    model_config = ConfigDict(frozen=True)

    rule_id: str
    passed: bool
    violation_message: str | None = None
    fix_suggestion: str | None = None


class RuleToolkitEngine:
    """RTK Engine evaluating AST rules and proposing automatic fixes."""

    def evaluate_rule_r001_domain_independent(self, code_content: str) -> RuleCheckResultDTO:
        """R-001: Domain Independent — Disallow framework imports."""
        forbidden = {"fastapi", "sqlalchemy", "openai", "httpx"}
        try:
            tree = ast.parse(code_content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        mod = alias.name.split(".")[0]
                        if mod in forbidden:
                            return RuleCheckResultDTO(
                                rule_id="R-001",
                                passed=False,
                                violation_message=(f"Forbidden import '{mod}' in domain"),
                                fix_suggestion=(f"Move import '{mod}' to adapter"),
                            )
        except SyntaxError as e:
            return RuleCheckResultDTO(
                rule_id="R-001",
                passed=False,
                violation_message=f"Syntax Error: {e}",
            )

        return RuleCheckResultDTO(
            rule_id="R-001",
            passed=True,
            violation_message=None,
            fix_suggestion=None,
        )
