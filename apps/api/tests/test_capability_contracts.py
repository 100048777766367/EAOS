"""Gateway capability contract registry tests."""

from apps.api.app.main import app
from apps.api.app.task_lifecycle import task_lifecycle_service
from fastapi.testclient import TestClient

client = TestClient(app)


def _capabilities() -> dict[str, dict[str, object]]:
    response = client.get("/v1/capabilities")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    return {item["capability_id"]: item for item in payload}


def test_capability_registry_exists_and_registers_known_contracts() -> None:
    capabilities = _capabilities()

    assert capabilities["gateway.health"]["status"] == "available"
    assert capabilities["capability.discovery"]["status"] == "available"
    assert capabilities["task.lifecycle"]["status"] == "available"
    task_paths = {endpoint["path"] for endpoint in capabilities["task.lifecycle"]["endpoints"]}
    assert "/api/v1/control/execute" in task_paths
    assert "/api/v1/tasks/{task_id}" in task_paths
    assert "/api/v1/tasks/{task_id}/events" in task_paths
    assert "websocket" in capabilities["task.lifecycle"]["transport"]


def test_capability_registry_represents_contract_gaps_without_fabricating_endpoints() -> None:
    capabilities = _capabilities()

    assert "unknown.fabricated" not in capabilities
    assert capabilities["digital_twin.dxs"]["status"] == "contract_gap"
    assert capabilities["digital_twin.dxs"]["endpoints"] == []
    assert capabilities["self_healing.loop"]["status"] == "contract_gap"
    assert capabilities["self_healing.loop"]["endpoints"] == []
    assert capabilities["spatial.future_interface"]["status"] == "contract_gap"


def test_capability_registry_declares_supported_status_vocabulary() -> None:
    capabilities = _capabilities()
    statuses = {item["status"] for item in capabilities.values()}

    assert "available" in statuses
    assert "contract_gap" in statuses
    assert statuses <= {"available", "degraded", "unavailable", "contract_gap"}
    assert "ready" not in statuses
    assert "success" not in statuses


def test_capability_discovery_does_not_execute_or_create_evidence() -> None:
    before_tasks = set(task_lifecycle_service._tasks)

    response = client.get("/v1/capabilities")

    after_tasks = set(task_lifecycle_service._tasks)
    assert response.status_code == 200
    assert after_tasks == before_tasks
    serialized = response.text.lower()
    assert "evidence_task_" not in serialized
    assert "governance-denied" not in serialized


def test_existing_task_lifecycle_and_websocket_remain_unchanged() -> None:
    created = client.post("/api/v1/control/execute", json={"command": "sync"}).json()
    task_id = created["task_id"]

    with client.websocket_connect(f"/api/v1/tasks/{task_id}/events") as websocket:
        states = []
        while True:
            try:
                states.append(websocket.receive_json()["lifecycle_state"])
            except Exception:
                break

    assert states == ["accepted", "planning", "executing", "verifying", "completed"]
