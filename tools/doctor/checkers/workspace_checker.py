from __future__ import annotations

from pathlib import Path

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel

"""Workspace Checker inspecting core enterprise files."""


class WorkspaceChecker:
    """Checker inspecting mandatory workspace governance files."""

    checker_id = "workspace"
    name = "Workspace Checker"
    category = "Workspace"
    version = "2.0.0"
    priority = 90
    enabled = True

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    def run(self) -> list[DiagnosticCheckDTO]:
        checks: list[DiagnosticCheckDTO] = []
        files = [
            ("Constitution", "ARCHITECTURE_CONSTITUTION.md"),
            ("ADR Registry", "docs/adr"),
            ("Pyproject Specs", "pyproject.toml"),
            ("README Document", "README.md"),
        ]

        for name, rel_path in files:
            target = self.root / rel_path
            exists = target.exists()
            status_str = "PASS" if exists else "WARN"
            severity = SeverityLevel.PASS if exists else SeverityLevel.WARN
            msg = f"Verified ({rel_path})" if exists else f"Uninitialized/Missing ({rel_path})"
            checks.append(
                DiagnosticCheckDTO(
                    checker_id=self.checker_id,
                    category=self.category,
                    name=name,
                    severity=severity,
                    status=status_str,
                    message=msg,
                )
            )

        return checks
