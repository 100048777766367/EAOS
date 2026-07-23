"""Unit test suite for EAOS deployable service unit health inspector."""

from pathlib import Path

from tools.services.service_health_inspector import ServiceHealthInspector

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_service_health_inspector_audits_all_8_services() -> None:
    """Verifies service health inspector discovers all 8 deployable units."""
    inspector = ServiceHealthInspector(ROOT_PATH)
    services = inspector.inspect_all_services()
    assert len(services) == 8
    svc_names = [s.service_name for s in services]
    assert "ai-service" in svc_names
    assert "knowledge-service" in svc_names
    assert "workflow-service" in svc_names
    assert all(s.health_check_passed for s in services)
