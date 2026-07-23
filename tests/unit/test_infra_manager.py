"""Unit test suite for EAOS infrastructure manager engine."""

from pathlib import Path

from tools.infra.infra_manager import InfraManagerEngine

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_infra_manager_audits_iac_manifests() -> None:
    """Verifies that infra manager discovers all 5 core IaC manifests."""
    engine = InfraManagerEngine(ROOT_PATH)
    audits = engine.audit_iac_manifests()
    assert len(audits) == 5
    services = [s.service_name for s in audits]
    assert "postgres" in services
    assert "redis" in services
    assert "prometheus" in services
    assert all(a.status == "CONFIGURED" for a in audits)
