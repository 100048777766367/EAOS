from __future__ import annotations

import tempfile
from pathlib import Path

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel

"""Filesystem Checker testing write permissions and directory structure."""


class FilesystemChecker:
    """Checker testing writable temporary directories and logs."""

    checker_id = "filesystem"
    name = "Filesystem & Permission Checker"
    category = "Filesystem"
    version = "2.0.0"
    priority = 30
    enabled = True

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    def run(self) -> list[DiagnosticCheckDTO]:
        checks: list[DiagnosticCheckDTO] = []
        dirs = [
            ("Runtime Workspace", "runtime"),
            ("Logs Workspace", "runtime/logs"),
            ("Pytest Temp Workspace", "runtime/tmp"),
            ("Generated Artifacts", "contracts/openapi"),
        ]

        for name, rel_path in dirs:
            target = self.root / rel_path
            target.mkdir(parents=True, exist_ok=True)
            is_writable = self._test_writable(target)

            checks.append(
                DiagnosticCheckDTO(
                    checker_id=self.checker_id,
                    category=self.category,
                    name=name,
                    severity=(SeverityLevel.PASS if is_writable else SeverityLevel.ERROR),
                    status="PASS" if is_writable else "FAIL",
                    message=(f"Writable ({rel_path})" if is_writable else f"Permission denied ({rel_path})"),
                )
            )

        return checks

    def _test_writable(self, target_dir: Path) -> bool:
        try:
            with tempfile.TemporaryFile(dir=str(target_dir)):
                return True
        except Exception:
            return False
