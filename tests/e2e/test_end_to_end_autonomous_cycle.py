"""End-to-End test suite verifying full autonomous cybernetic cycle."""

from apps.api.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_e2e_autonomous_cycle_execution() -> None:
    """Verifies E2E cybernetic evolution loop execution."""
    payload = {
        "problem": "E2E Test: Memory spike in Splay Cache",
        "author": "E2ETester",
    }
    response = client.post("/autonomous/run-cycle", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] in ["SUCCESS", "cycle_complete"]
