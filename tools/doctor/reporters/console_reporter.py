from __future__ import annotations

from typing import Any

from tools.doctor.dto import DiagnosticReportDTO, SeverityLevel

"""Console Formatter for Enterprise Doctor Report."""


class ConsoleReporter:
    """Formats DiagnosticReportDTO into rich CLI output."""

    def render(self, report: DiagnosticReportDTO) -> str:
        lines = [
            "EAOS Enterprise Doctor v2",
            "========================",
            "",
        ]

        categories: dict[str, list[Any]] = {}
        for check in report.checks:
            categories.setdefault(check.category, []).append(check)

        for cat_name, checks in categories.items():
            lines.append(cat_name)
            lines.append("-" * 16)
            lines.extend([f"{c.status:<4} {c.name:<25} ({c.message})" for c in checks])
            lines.append("")

        warns = sum(1 for c in report.checks if c.status == "WARN")
        errs = sum(1 for c in report.checks if c.severity == SeverityLevel.ERROR)
        crits = sum(1 for c in report.checks if c.severity == SeverityLevel.CRITICAL)

        lines.append("-" * 40)
        lines.append(f"Total checks : {report.total_checks}")
        lines.append(f"Passed       : {report.passed_checks}")
        lines.append(f"Failed       : {report.failed_checks}")
        lines.append(f"Warnings     : {warns}")
        lines.append(f"Errors       : {errs}")
        lines.append(f"Criticals    : {crits}")
        lines.append("")
        lines.append(f"Overall Health Score : {report.overall_health_score}")
        lines.append(f"Enterprise Readiness : {report.status}")

        return "\n".join(lines)
