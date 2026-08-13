"""Integration tests for Runtime Control Plane API endpoints and WebSocket protocol."""

import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_runtime_control_status_endpoint(client: TestClient) -> None:
    """Verify /v1/runtime/control/status endpoint."""
    res = client.get("/v1/runtime/control/status")
    assert res.status_code == 200
    data = res.json()
    assert "system_health" in data
    assert "processes" in data
    assert "graph_nodes" in data
    assert len(data["graph_nodes"]) == 9


def test_runtime_control_processes_endpoint(client: TestClient) -> None:
    """Verify /v1/runtime/control/processes endpoint."""
    res = client.get("/v1/runtime/control/processes")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    assert any(p["capability_name"] == "api_gateway" for p in data)


def test_runtime_control_task_lifecycle_and_recovery(client: TestClient) -> None:
    """Verify task query and recovery API flow."""
    # Trigger recovery endpoint for a task
    res_rec = client.post("/v1/runtime/control/recover/tsk-integration-01?component=test_suite")
    assert res_rec.status_code == 200
    rec_data = res_rec.json()
    assert rec_data["task_id"] == "tsk-integration-01"
    assert "failure_classified" in rec_data
    assert "recovery_outcome" in rec_data

    # Query task lifecycle status
    res_task = client.get("/v1/runtime/control/tasks/tsk-integration-01")
    assert res_task.status_code == 200
    task_data = res_task.json()
    assert task_data["task_id"] == "tsk-integration-01"
    assert "current_state" in task_data
    assert "proof_hash" in task_data


def test_websocket_chat_lifecycle_protocol(client: TestClient) -> None:
    """Verify WebSocket /ws/chat frame exchange lifecycle and correlation."""
    with client.websocket_connect("/ws/chat") as websocket:
        # Send goal request
        payload = {
            "conversation_id": "conv-test-ws",
            "message": "Inspect runtime control plane status",
            "agent_role": "coder",
        }
        websocket.send_json(payload)

        # Receive QUEUED state frame
        frame_queued = websocket.receive_json()
        assert frame_queued["type"] == "task_lifecycle"
        assert frame_queued["state"] == "QUEUED"
        assert "correlation" in frame_queued
        assert "proof_hash" in frame_queued

        # Receive RUNNING state frame
        frame_running = websocket.receive_json()
        assert frame_running["type"] == "task_lifecycle"
        assert frame_running["state"] == "RUNNING"
