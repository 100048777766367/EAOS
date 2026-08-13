from __future__ import annotations

import os
from pathlib import Path

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel

"""Security Checker inspecting environment variables and secrets."""


class SecurityChecker:
    """Checker inspecting security posture and environment config."""

    checker_id = "security"
    name = "Security Checker"
    category = "Security"
    version = "2.0.0"
    priority = 20
    enabled = True

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()

    def run(self) -> list[DiagnosticCheckDTO]:
        checks: list[DiagnosticCheckDTO] = []

        env_file = self.root / ".env"
        env_exists = env_file.exists()
        db_url_set = False

        if env_exists:
            content = env_file.read_text(encoding="utf-8")
            if "DATABASE_URL" in content:
                db_url_set = True

        if not db_url_set:
            db_url_set = bool(os.getenv("DATABASE_URL"))

        checks.append(
            DiagnosticCheckDTO(
                checker_id=self.checker_id,
                category=self.category,
                name="Environment Config",
                severity=SeverityLevel.PASS if env_exists else SeverityLevel.WARN,
                status="PASS" if env_exists else "WARN",
                message=("Loaded (.env)" if env_exists else "Using defaults"),
            )
        )

        checks.append(
            DiagnosticCheckDTO(
                checker_id=self.checker_id,
                category=self.category,
                name="Database URL Secret",
                severity=(SeverityLevel.PASS if db_url_set else SeverityLevel.WARN),
                status="PASS" if db_url_set else "WARN",
                message="Configured (.env)" if db_url_set else "Unset in .env",
            )
        )

        return checks
