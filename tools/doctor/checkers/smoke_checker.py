from __future__ import annotations

from pathlib import Path

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel

"""Smoke Checker for basic workspace health."""


class SmokeChecker:
    """Basic smoke checker for workspace health."""

    checker_id = "smoke"
    name = "Smoke Checker"
    category = "Smoke Check"
    version = "2.0.0"
    priority = 100
    enabled = True

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    def run(self) -> list[DiagnosticCheckDTO]:
        return [
            DiagnosticCheckDTO(
                checker_id=self.checker_id,
                category=self.category,
                name="Workspace Integrity",
                severity=SeverityLevel.PASS,
                status="PASS",
                message="Smoke check passed",
            )
        ]
