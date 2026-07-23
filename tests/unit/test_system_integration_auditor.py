"""Unit test suite for system integration auditor."""

from pathlib import Path

from tools.graph.system_integration_auditor import (
    SystemIntegrationAuditor,
)

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_system_integration_auditor_verifies_100_percent_connectivity() -> None:
    """Verifies that all defined root directories are active and participating."""
    auditor = SystemIntegrationAuditor(ROOT_PATH)
    connectivities = auditor.audit_system_connectivity()
    assert len(connectivities) >= 38
    assert all(c.is_participating for c in connectivities)
