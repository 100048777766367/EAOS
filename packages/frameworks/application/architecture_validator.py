from pathlib import Path

from pydantic import BaseModel, ConfigDict

from packages.frameworks.domain.rule_toolkit import RuleToolkitEngine

"""Sprint 6 Engine: Executable Architecture Validator & Scorecard."""


class ValidationReportDTO(BaseModel):
    """Value object representing full architecture validation report."""

    model_config = ConfigDict(frozen=True)

    total_files_audited: int
    rules_checked: int
    violations_found: int
    fitness_score: float
    is_compliant: bool


class ExecutableArchitectureValidator:
    """Validator inspecting repository against Executable Rules."""

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()
        self.rtk = RuleToolkitEngine()

    def validate_repository(self) -> ValidationReportDTO:
        """Audits domain packages in repository against RTK rules."""
        domain_files = list(self.root_path.glob("packages/*/domain/*.py"))
        violations = 0

        for df in domain_files:
            code = df.read_text(encoding="utf-8")
            res = self.rtk.evaluate_rule_r001_domain_independent(code)
            if not res.passed:
                violations += 1

        total = len(domain_files)
        score = ((total - violations) / total * 100.0) if total > 0 else 100.0

        return ValidationReportDTO(
            total_files_audited=total,
            rules_checked=1,
            violations_found=violations,
            fitness_score=round(score, 2),
            is_compliant=(violations == 0),
        )
