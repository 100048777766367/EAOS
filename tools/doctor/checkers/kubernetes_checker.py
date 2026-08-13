from __future__ import annotations

import shutil

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel

"""Extensible Kubernetes Cluster Checker Placeholder."""


class KubernetesChecker:
    """Checker inspecting kubectl CLI and cluster connectivity."""

    checker_id = "kubernetes"
    name = "Kubernetes Cluster Checker"
    category = "Infrastructure"
    version = "2.0.0"
    priority = 48
    enabled = True

    def run(self) -> list[DiagnosticCheckDTO]:
        kubectl = shutil.which("kubectl")
        status = "PASS" if kubectl else "INFO"
        sev = SeverityLevel.PASS if kubectl else SeverityLevel.INFO
        msg = f"kubectl available ({kubectl})" if kubectl else "Local mode (No kubectl)"

        return [
            DiagnosticCheckDTO(
                checker_id=self.checker_id,
                category=self.category,
                name="Kubernetes CLI",
                severity=sev,
                status=status,
                message=msg,
            )
        ]
