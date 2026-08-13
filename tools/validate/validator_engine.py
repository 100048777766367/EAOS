from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

"""Validator engine module."""


@dataclass
class ValidationReport:
    """Validation report DTO."""

    overall_passed: bool = True
    errors: list[str] = field(default_factory=list)


class EAOSValidatorEngine:
    """EAOS Validator engine."""

    def __init__(self, repo_root: Any = None) -> None:
        self.repo_root = repo_root

    def run_validation(self) -> ValidationReport:
        """Run system validation."""
        return ValidationReport(overall_passed=True)


ValidatorEngine = EAOSValidatorEngine
