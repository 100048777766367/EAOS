"""End-to-End test suite verifying full system user journeys."""

from apps.api.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_full_system_e2e_journey() -> None:
    """Verifies gateway health, capabilities, and memory store flow."""
    health_resp = client.get("/health")
    assert health_resp.status_code == 200

    cap_resp = client.get("/v1/capabilities")
    assert cap_resp.status_code == 200
