from __future__ import annotations

import urllib.request
from typing import ClassVar

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel

"""AI Runtime Checker probing Ollama and OpenWebUI."""


class AIChecker:
    """Checker probing AI models, Ollama, and OpenWebUI."""

    checker_id = "ai_runtime"
    name = "AI Runtime Checker"
    category = "AI Runtime"
    version = "2.0.0"
    priority = 80
    enabled = True

    SERVICES: ClassVar[tuple[tuple[str, str], ...]] = (
        ("Ollama Local AI", "http://localhost:11434/api/tags"),
        ("OpenWebUI (Docker)", "http://localhost:3001/"),
    )

    def run(self) -> list[DiagnosticCheckDTO]:
        checks: list[DiagnosticCheckDTO] = []

        for name, url in self.SERVICES:
            healthy = self._check_http(url)
            checks.append(
                DiagnosticCheckDTO(
                    checker_id=self.checker_id,
                    category=self.category,
                    name=name,
                    severity=(SeverityLevel.PASS if healthy else SeverityLevel.WARN),
                    status="PASS" if healthy else "WARN",
                    message=(f"Online ({url})" if healthy else f"Offline ({url})"),
                )
            )

        return checks

    def _check_http(self, url: str) -> bool:
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                return resp.status in (200, 204)
        except Exception:
            return False
