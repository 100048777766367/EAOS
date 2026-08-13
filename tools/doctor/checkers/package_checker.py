from __future__ import annotations

from pathlib import Path

from tools.doctor.dto import DiagnosticCheckDTO

"""Package Checker inspecting monorepo package structure."""


class PackageChecker:
    """Checker inspecting packages/ and apps/ structure."""

    checker_id = "packages"
    name = "Monorepo Package Architecture Checker"
    category = "Architecture"
    version = "2.0.0"
    priority = 35
    enabled = True

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    def run(self) -> list[DiagnosticCheckDTO]:
        checks: list[DiagnosticCheckDTO] = []

        for folder in ["packages", "apps"]:
            target = self.root / folder
            count = len([p for p in target.iterdir() if p.is_dir()]) if target.exists() else 0
            checks.append(
                DiagnosticCheckDTO(
                    checker_id=self.checker_id,
                    category=self.category,
                    name=f"{folder.title()} Monorepo",
                    status="PASS" if count > 0 else "WARN",
                    message=f"{count} packages detected",
                )
            )

        return checks
