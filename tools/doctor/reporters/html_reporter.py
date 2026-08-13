from __future__ import annotations

from tools.doctor.dto import DiagnosticReportDTO

"""HTML Formatter for Enterprise Doctor Report."""


class HTMLReporter:
    """Formats DiagnosticReportDTO into HTML document."""

    def render(self, report: DiagnosticReportDTO) -> str:
        lines = [
            "<!DOCTYPE html><html><head><title>EAOS Doctor Report</title>",
            "<style>body{font-family:sans-serif;background:#020617;",
            "color:#f8fafc;padding:20px;}</style></head><body>",
            "<h1>EAOS Enterprise Doctor Report</h1>",
            f"<h2>Score: {report.overall_health_score}/100 - Status: {report.status}</h2>",
            "<table border='1' cellpadding='8'>",
            "<tr><th>Category</th><th>Check</th><th>Status</th><th>Message</th></tr>",
        ]

        lines.extend(
            [
                f"<tr><td>{c.category}</td><td>{c.name}</td><td>{c.status}</td><td>{c.message}</td></tr>"
                for c in report.checks
            ]
        )

        lines.append("</table></body></html>")
        return "\n".join(lines)
