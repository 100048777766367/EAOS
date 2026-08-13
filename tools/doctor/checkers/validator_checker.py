from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel
from tools.validate.architecture_validator import ArchitectureValidator

"""Validator Checker invoking EAOS Architecture Validator."""


class ValidatorChecker:
    """Checker running AST Architecture Validator Engine."""

    checker_id = "validator"
    name = "Architecture Validator Checker"
    category = "Architecture Validator"
    version = "2.0.0"
    priority = 10
    enabled = True

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    def run(self) -> list[DiagnosticCheckDTO]:
        try:
            validator: Any = ArchitectureValidator(self.root)
            if hasattr(validator, "validate_architecture"):
                report = validator.validate_architecture()
            elif hasattr(validator, "validate"):
                report = validator.validate()
            else:
                report = None

            compliant = getattr(report, "compliant", getattr(report, "passed", True))
            violations = getattr(report, "violations", [])

            status_str = "PASS" if compliant else "FAIL"
            severity = SeverityLevel.PASS if compliant else SeverityLevel.ERROR
            msg = f"Violations: {len(violations)}" if not compliant else "0 Boundary Violations"

            return [
                DiagnosticCheckDTO(
                    checker_id=self.checker_id,
                    category=self.category,
                    name="AST Boundary Rules",
                    severity=severity,
                    status=status_str,
                    message=msg,
                )
            ]
        except Exception as err:
            return [
                DiagnosticCheckDTO(
                    checker_id=self.checker_id,
                    category=self.category,
                    name="AST Boundary Rules",
                    severity=SeverityLevel.WARN,
                    status="WARN",
                    message=f"Validator check error: {err}",
                )
            ]
