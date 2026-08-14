from pathlib import Path

from dxs.diagnostics.engine import DiagnosticEngine


def test_diagnostic_engine():
    engine = DiagnosticEngine()

    report = engine.run(Path("."))

    assert len(report.items) >= 4
    assert report.score == 100
