"""Unit test suite for EAOS test suite auditor engine."""

from pathlib import Path

from tools.testing.test_suite_orchestrator import TestSuiteAuditorEngine

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_suite_orchestrator_audits_all_5_tiers() -> None:
    """Verifies that auditor engine evaluates all 5 testing pyramid tiers."""
    auditor = TestSuiteAuditorEngine(ROOT_PATH)
    summaries = auditor.audit_test_tiers()
    assert len(summaries) == 5
    tiers = [s.tier for s in summaries]
    assert "contract" in tiers
    assert "e2e" in tiers
    assert "integration" in tiers
    assert "performance" in tiers
    assert "unit" in tiers
    assert all(s.file_count >= 0 for s in summaries)
