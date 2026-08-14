from __future__ import annotations

from pathlib import Path

from dxs.diagnostics.checks import (
    architecture_check,
    evidence_check,
    health_check,
    repository_check,
)
from dxs.diagnostics.report import (
    DiagnosticReport,
)


class DiagnosticEngine:
    def run(
        self,
        root: Path,
    ) -> DiagnosticReport:
        report = DiagnosticReport()

        checks = [
            architecture_check(root),
            repository_check(root),
            health_check(),
            evidence_check(),
        ]

        for check in checks:
            report.add(
                name=check["name"],
                status=check["status"],
                message=check["message"],
            )

        return report
