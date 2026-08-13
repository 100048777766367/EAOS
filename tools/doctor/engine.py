from __future__ import annotations

from pathlib import Path

from tools.doctor.dto import DiagnosticCheckDTO, DiagnosticReportDTO
from tools.doctor.registry import CheckerRegistry

"""EAOS Doctor Orchestration Engine (SOLID OCP)."""


class EAOSDoctorEngine:
    """Orchestrator invoking registered checkers without knowing details."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.registry = CheckerRegistry(self.root)

    def diagnose_system(self) -> DiagnosticReportDTO:
        """Run all registered diagnostic checkers and assemble report."""
        all_checks: list[DiagnosticCheckDTO] = []
        ast_compliant = True

        for checker in self.registry.get_checkers():
            checks = checker.run()
            all_checks.extend(checks)
            for c in checks:
                if c.category == "Architecture Validator" and c.status == "FAIL":
                    ast_compliant = False

        passed = sum(1 for c in all_checks if c.status == "PASS")
        failed = sum(1 for c in all_checks if c.status == "FAIL")

        total = len(all_checks)
        health_score = int((passed / total) * 100) if total > 0 else 100

        unique_categories = sorted({c.category for c in all_checks if c.category})

        status = "READY" if failed == 0 and ast_compliant else "UNHEALTHY"

        return DiagnosticReportDTO(
            status=status,
            overall_health_score=health_score,
            total_checks=total,
            passed_checks=passed,
            failed_checks=failed,
            checks=all_checks,
            categories=unique_categories,
            ast_compliant=ast_compliant,
        )
