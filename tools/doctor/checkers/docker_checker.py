from __future__ import annotations

import subprocess
from typing import ClassVar

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel

"""Docker Container Daemon Checker for EAOS Canonical Stack."""


class DockerChecker:
    """Checker inspecting Docker Engine and canonical containers."""

    checker_id = "docker"
    name = "Docker Daemon Checker"
    category = "Docker Infrastructure"
    version = "2.0.0"
    priority = 35
    enabled = True

    CANONICAL_CONTAINERS: ClassVar[tuple[str, ...]] = (
        "eaos-postgres",
        "eaos-redis",
        "eaos-neo4j",
        "eaos-minio",
        "eaos-qdrant",
        "eaos-ollama",
        "eaos-prometheus",
        "eaos-grafana",
    )

    def run(self) -> list[DiagnosticCheckDTO]:
        checks: list[DiagnosticCheckDTO] = []

        engine_active = self._check_docker_engine()
        checks.append(
            DiagnosticCheckDTO(
                checker_id=self.checker_id,
                category=self.category,
                name="Docker Engine Service",
                severity=(SeverityLevel.PASS if engine_active else SeverityLevel.WARN),
                status="PASS" if engine_active else "WARN",
                message=("Docker Engine Active" if engine_active else "Docker Engine Offline"),
            )
        )

        if engine_active:
            running = self._get_running_containers()
            for c_name in self.CANONICAL_CONTAINERS:
                is_running = c_name in running
                checks.append(
                    DiagnosticCheckDTO(
                        checker_id=self.checker_id,
                        category=self.category,
                        name=f"Container: {c_name}",
                        severity=(SeverityLevel.PASS if is_running else SeverityLevel.WARN),
                        status="PASS" if is_running else "WARN",
                        message=("Container Running (24/7)" if is_running else "Container Stopped/Not Deployed"),
                    )
                )

        return checks

    def _check_docker_engine(self) -> bool:
        try:
            res = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=5,
            )
            return res.returncode == 0
        except Exception:
            return False

    def _get_running_containers(self) -> set[str]:
        try:
            res = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0:
                return set(res.stdout.splitlines())
            return set()
        except Exception:
            return set()
