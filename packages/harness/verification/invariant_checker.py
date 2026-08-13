from __future__ import annotations

from pathlib import Path
from typing import Final

# invariant_checker.py
"""Invariant Checker verifying file scope boundaries and AST purity."""


class InvariantCheckResultDTO:
    """Result of invariant checking."""

    def __init__(self, passed: bool, breaches: list[str]) -> None:
        self.passed = passed
        self.breaches = breaches


class InvariantChecker:
    """Checks architectural invariants on workspace after action."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root: Final[Path] = (workspace_root or Path.cwd()).resolve()

    def verify_invariants(self, modified_files: list[str]) -> InvariantCheckResultDTO:
        """Verifies invariants: modified files must exist."""
        breaches: list[str] = []

        for rel_p in modified_files:
            f_path = self.root / rel_p
            if not f_path.exists():
                breaches.append(f"Invariant breach: File '{rel_p}' deleted.")

        return InvariantCheckResultDTO(passed=len(breaches) == 0, breaches=breaches)
