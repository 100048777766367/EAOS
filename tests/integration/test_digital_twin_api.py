"""Integration tests for Digital Twin System Graph API endpoints."""

import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_digitaltwin_graph_endpoint(client: TestClient) -> None:
    """Verify /v1/digitaltwin/graph endpoint."""
    res = client.get("/v1/digitaltwin/graph")
    assert res.status_code == 200
    data = res.json()
    assert "twin_id" in data
    assert data["total_nodes"] > 0
    assert data["total_edges"] > 0
    assert "provenance_summary" in data


def test_digitaltwin_impact_endpoint(client: TestClient) -> None:
    """Verify /v1/digitaltwin/impact analysis endpoint."""
    payload = {"target_file": "apps/api/app/container.py"}
    res = client.post("/v1/digitaltwin/impact", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["target_file"] == "apps/api/app/container.py"
    assert data["blast_radius"] == "SYSTEMIC"
    assert data["crosses_architecture_boundary"] is True
    assert "recommended_test_suites" in data


def test_digitaltwin_consistency_endpoint(client: TestClient) -> None:
    """Verify /v1/digitaltwin/consistency endpoint."""
    res = client.get("/v1/digitaltwin/consistency")
    assert res.status_code == 200
    data = res.json()
    assert "is_consistent" in data
    assert "violations" in data


def test_digitaltwin_delta_endpoint(client: TestClient) -> None:
    """Verify /v1/digitaltwin/delta endpoint."""
    payload = {"before_snapshot_name": "NON_EXISTENT_SNAPSHOT", "max_allowed_node_delta": 5}
    res = client.post("/v1/digitaltwin/delta", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "checkpoint_id" in data
    assert data["exceeds_prediction"] is False
