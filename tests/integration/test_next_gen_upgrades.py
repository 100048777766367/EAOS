import pytest
from apps.api.app.main import app, policy_evaluator
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_four_infrastructure_upgrades_flow(client: TestClient) -> None:
    # 1. TEST UPGRADE 1: Dynamic Policy Engine
    reload_resp = client.post("/governance/policy/reload")
    assert reload_resp.status_code == 200
    assert reload_resp.json()["status"] == "RELOADED"

    passed, results = policy_evaluator.evaluate_payload({"__version": 2})
    assert passed is True
    assert len(results) == 3

    # 2. TEST UPGRADE 2: Live Telemetry Daemon
    telemetry_payload = {
        "metric_name": "API_p99_latency",
        "value": 650.0,
        "unit": "ms",
    }
    telem_resp = client.post("/telemetry/ingest", json=telemetry_payload)
    assert telem_resp.status_code == 200
    telem_data = telem_resp.json()
    assert telem_data["status"] == "DEGRADATION_DETECTED"
    assert telem_data["triggered_reflection_id"].startswith("REF-")

    # 3. TEST UPGRADE 3: GitOps Driver
    gitops_payload = {
        "branch_name": "feature/test-gitops-auto-fix",
        "file_path": "README.md",
        "diff_content": "+ Auto fix line",
        "commit_message": "fix(auto): apply self-heal patch",
    }
    gitops_resp = client.post("/gitops/apply-pr", json=gitops_payload)
    assert gitops_resp.status_code == 200
    assert gitops_resp.json()["status"] == "GIT_BRANCH_AND_COMMIT_CREATED"

    # 4. TEST UPGRADE 4: Capability Pack Hot-Loader
    hotplug_resp = client.post("/capabilities/hot-plug")
    assert hotplug_resp.status_code == 200
    assert hotplug_resp.json()["status"] == "HOT_PLUG_COMPLETED"
