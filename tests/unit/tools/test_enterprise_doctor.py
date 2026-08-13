from __future__ import annotations

from pathlib import Path

from tools.doctor.engine import EAOSDoctorEngine
from tools.doctor.reporters.console_reporter import ConsoleReporter
from tools.doctor.reporters.json_reporter import JSONReporter

"""Unit test suite for Enterprise Doctor System."""


def test_doctor_engine_diagnosis(tmp_path: Path) -> None:
    """Test doctor engine runs checkers and computes report."""
    engine = EAOSDoctorEngine(workspace_root=tmp_path)
    report = engine.diagnose_system()

    assert report.total_checks > 0
    assert report.overall_health_score >= 0
    assert len(report.checks) == report.total_checks
    assert len(report.categories) > 0


def test_doctor_reporters(tmp_path: Path) -> None:
    """Test console and json reporters render DTO."""
    engine = EAOSDoctorEngine(workspace_root=tmp_path)
    report = engine.diagnose_system()

    console_out = ConsoleReporter().render(report)
    assert "EAOS Enterprise Doctor" in console_out

    json_out = JSONReporter().render(report)
    assert '"overall_health_score"' in json_out
