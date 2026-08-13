"""Integration tests for Agent Capability Registry & Orchestration API endpoints."""

import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_get_agent_registry_endpoint(client: TestClient) -> None:
    """Verify /v1/agents/registry endpoint."""
    res = client.get("/v1/agents/registry")
    assert res.status_code == 200
    data = res.json()
    assert data["capabilities_count"] > 0
    assert data["agents_count"] > 0
    assert "capabilities" in data
    assert "agents" in data


def test_select_agents_endpoint(client: TestClient) -> None:
    """Verify /v1/agents/select capability matching endpoint."""
    payload = {
        "task_id": "tsk-api-01",
        "intent": "Optimize API route handler",
        "task_type": "patch",
        "required_authority": "L2",
        "blast_radius": "LOCAL",
    }
    res = client.post("/v1/agents/select", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["task_id"] == "tsk-api-01"
    assert data["is_blocked_by_governance"] is False
    assert data["primary_implementer_agent"] is not None


def test_orchestrate_workflow_endpoint(client: TestClient) -> None:
    """Verify /v1/agents/orchestrate multi-agent workflow endpoint."""
    payload = {
        "task_id": "tsk-api-wf",
        "intent": "Update API configuration file",
        "task_type": "patch",
        "required_authority": "L2",
        "target_files": ["apps/api/app/settings.py"],
        "blast_radius": "LOCAL",
    }
    res = client.post("/v1/agents/orchestrate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["task_id"] == "tsk-api-wf"
    assert data["overall_success"] is True
    assert data["steps_executed"] == 2
    assert "evidence_token" in data


def test_get_active_locks_endpoint(client: TestClient) -> None:
    """Verify /v1/agents/locks endpoint."""
    res = client.get("/v1/agents/locks")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
