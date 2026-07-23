"""Unit test suite for EAOS multi-format artifact exporter."""

from pathlib import Path

from tools.exporter.artifact_exporter import ArtifactExporterEngine

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_artifact_exporter_engine_exports_all_formats() -> None:
    """Verifies that exporter writes artifacts across multiple formats."""
    exporter = ArtifactExporterEngine(ROOT_PATH)
    artifacts = exporter.export_all_formats({"system_id": "TEST-SYS"})
    assert len(artifacts) == 3
    formats = [a.format_type for a in artifacts]
    assert "JSON" in formats
    assert "MERMAID" in formats
    assert "WEBSITE_HTML" in formats
