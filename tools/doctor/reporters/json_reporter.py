from __future__ import annotations

from tools.doctor.dto import DiagnosticReportDTO

"""JSON Formatter for EAOS Doctor Report."""


class JSONReporter:
    """Formats DiagnosticReportDTO into JSON string."""

    def render(self, report: DiagnosticReportDTO) -> str:
        return report.model_dump_json(indent=2)
