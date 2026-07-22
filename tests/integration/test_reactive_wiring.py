"""Integration test for Reactive Event Wiring and Policy Middleware."""

import pytest
from apps.api.app.main import app, knowledge_graph_adapter, self_rewrite_repo
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_policy_middleware_blocking_invalid_header(client: TestClient) -> None:
    # Send request with invalid environment header -> Should be blocked (403)
    response = client.post(
        "/events/publish/degraded-health",
        json={
            "capability_id": "packages/knowledge",
            "current_health_score": 65.0,
            "drift_index": 0.20,
        },
        headers={"X-Environment": "staging"},
    )
    assert response.status_code == 403
    assert "Request rejected by EAOS Policy Engine" in response.json()["detail"]


def test_reactive_metrics_to_self_rewrite_and_graph_chain(
    client: TestClient,
) -> None:
    # 1. Send valid health degraded event -> Triggers Policy ALLOW (202)
    response = client.post(
        "/events/publish/degraded-health",
        json={
            "capability_id": "packages/knowledge",
            "current_health_score": 65.0,
            "drift_index": 0.20,
        },
        headers={"X-Environment": "production"},
    )
    assert response.status_code == 202

    # 2. Verify Reactive Chain: Kaizen Initiative automatically triggered Self-Rewrite Job
    jobs = self_rewrite_repo.list_all()
    assert len(jobs) == 1
    assert "Auto-Kaizen" in jobs[0].problem
    assert jobs[0].status == "SUCCESS"

    # 3. Verify Knowledge Graph Auto-Ingestion
    graph = knowledge_graph_adapter.find_by_id("GLOBAL-GRAPH")
    assert graph is not None
