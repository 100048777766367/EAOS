from __future__ import annotations

from tools.doctor.dto import DiagnosticReportDTO

"""Markdown Formatter for Enterprise Doctor Report."""


class MarkdownReporter:
    """Formats DiagnosticReportDTO into Markdown document."""

    def render(self, report: DiagnosticReportDTO) -> str:
        lines = [
            "# EAOS Enterprise Diagnostic Report",
            "",
            f"**Overall Health Score:** {report.overall_health_score}/100",
            f"**Enterprise Readiness:** {report.status}",
            "",
            "| Category | Check | Status | Details |",
            "| :--- | :--- | :--- | :--- |",
        ]

        lines.extend([f"| {c.category} | {c.name} | `{c.status}` | {c.message} |" for c in report.checks])

        return "\n".join(lines)
