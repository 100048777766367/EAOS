"""Gateway task lifecycle contract tests."""

from apps.api.app.routers.tasks import router
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def _submit(command: str, target_agent: str = "planner") -> dict[str, object]:
    response = client.post(
        "/api/v1/control/execute",
        json={"command": command, "target_agent": target_agent},
    )
    assert response.status_code == 200
    return response.json()


def test_task_creation_status_completion_and_evidence() -> None:
    created = _submit("doctor")
    assert created["task_id"].startswith("task_")
    assert created["lifecycle_state"] == "completed"
    assert created["metadata"]["evidence"]["evidence_id"]

    status = client.get(f"/api/v1/tasks/{created['task_id']}")
    assert status.status_code == 200
    payload = status.json()
    assert payload["lifecycle_state"] == "completed"
    assert payload["verification"]["passed"] is True
    assert payload["evidence"]["task_id"] == created["task_id"]


def test_lifecycle_transitions_and_websocket_events() -> None:
    created = _submit("sync")
    task_id = created["task_id"]
    with client.websocket_connect(f"/api/v1/tasks/{task_id}/events") as websocket:
        states = []
        while True:
            try:
                states.append(websocket.receive_json()["lifecycle_state"])
            except Exception:
                break
    assert states == ["accepted", "planning", "executing", "verifying", "completed"]


def test_governance_denied() -> None:
    created = _submit("deny this change")
    assert created["lifecycle_state"] == "denied"
    assert created["metadata"]["governance"]["allow"] is False
    assert created["metadata"]["evidence"]["kind"] == "governance-denied"


def test_execution_failure() -> None:
    created = _submit("fail")
    assert created["lifecycle_state"] == "failed"
    assert created["metadata"]["error"]["type"] == "ValueError"


def test_verification_failure() -> None:
    created = _submit("verify-fail")
    assert created["lifecycle_state"] == "failed"
    assert created["metadata"]["verification"]["passed"] is False


def test_unknown_task_and_malformed_request() -> None:
    assert client.get("/api/v1/tasks/missing").status_code == 404
    response = client.post("/api/v1/control/execute", json={"command": ""})
    assert response.status_code == 422
