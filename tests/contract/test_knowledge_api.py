"""Contract tests for Knowledge Architecture REST API endpoints."""

from apps.api.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_topology_contract() -> None:
    """Verify topology contract returns required keys."""
    response = client.get("/api/v1/knowledge/topology")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "relationships" in data
    assert "node_count" in data
    assert "relationship_count" in data


def test_get_nodes_by_category_contract() -> None:
    """Verify category filtering endpoint contract."""
    response = client.get("/api/v1/knowledge/nodes/SERVICE")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    invalid_resp = client.get("/api/v1/knowledge/nodes/INVALID_CATEGORY_NAME")
    assert invalid_resp.status_code == 400
    assert "Invalid node category" in invalid_resp.json()["detail"]


def test_get_node_lineage_contract() -> None:
    """Verify node lineage contract."""
    response = client.get("/api/v1/knowledge/lineage/CAP-001?depth=2")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "relationships" in data


def test_get_knowledge_health_contract() -> None:
    """Verify knowledge health contract."""
    response = client.get("/api/v1/knowledge/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ("ok", "unhealthy")
