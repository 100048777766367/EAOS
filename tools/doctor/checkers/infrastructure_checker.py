from __future__ import annotations

import socket
import urllib.request
from typing import ClassVar

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel

"""Infrastructure Checker with Deep Application Probes."""


class InfrastructureChecker:
    """Checker performing HTTP/TCP deep probes for DBs and storage."""

    checker_id = "infrastructure"
    name = "Infrastructure Deep Probe Checker"
    category = "Infrastructure"
    version = "2.0.0"
    priority = 40
    enabled = True

    SERVICES: ClassVar[tuple[tuple[str, str, int, str | None], ...]] = (
        ("PostgreSQL (pgvector)", "localhost", 5433, None),
        ("Redis Cache", "localhost", 6380, None),
        ("Neo4j Graph DB", "localhost", 7474, "http://localhost:7474"),
        (
            "MinIO Storage",
            "localhost",
            9001,
            "http://localhost:9000/minio/health/live",
        ),
        (
            "Qdrant Vector DB",
            "localhost",
            6333,
            "http://localhost:6333/healthz",
        ),
    )

    def run(self) -> list[DiagnosticCheckDTO]:
        checks: list[DiagnosticCheckDTO] = []

        for name, host, port, probe_url in self.SERVICES:
            healthy, msg = self._probe_service(host, port, probe_url)
            sev = SeverityLevel.PASS if healthy else SeverityLevel.WARN
            checks.append(
                DiagnosticCheckDTO(
                    checker_id=self.checker_id,
                    category=self.category,
                    name=name,
                    severity=sev,
                    status="PASS" if healthy else "WARN",
                    message=msg,
                )
            )

        return checks

    def _probe_service(self, host: str, port: int, probe_url: str | None) -> tuple[bool, str]:
        if probe_url:
            try:
                req = urllib.request.Request(probe_url, method="GET")
                with urllib.request.urlopen(req, timeout=1.0) as resp:
                    if resp.status in (200, 204):
                        return True, f"HTTP Healthy ({probe_url})"
            except Exception:
                pass

        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True, f"TCP Socket Open ({host}:{port})"
        except Exception:
            return False, f"Service Offline ({host}:{port})"
