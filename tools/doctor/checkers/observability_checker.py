from __future__ import annotations

import urllib.request
from typing import ClassVar

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel

"""Observability Checker for Prometheus, Grafana, and OTLP."""


class ObservabilityChecker:
    """Checker probing Prometheus, Grafana, and telemetry endpoints."""

    checker_id = "observability"
    name = "Observability Checker"
    category = "Observability"
    version = "2.0.0"
    priority = 50
    enabled = True

    SERVICES: ClassVar[tuple[tuple[str, str], ...]] = (
        ("Prometheus UI", "http://localhost:9090/-/healthy"),
        ("Grafana Dashboard", "http://localhost:3000/api/health"),
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
