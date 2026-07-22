import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_production_four_upgrades_integration_suite(
    client: TestClient,
) -> None:
    # 1. Test Nâng cấp 1: OPA Dynamic Policy Engine
    opa_payload = {"input_data": {"__version": 2, "environment": "production"}}
    opa_resp = client.post("/governance/opa/evaluate", json=opa_payload)
    assert opa_resp.status_code == 200
    opa_data = opa_resp.json()
    assert opa_data["allow"] is True
    assert "metrics" in opa_data

    # 2. Test Nâng cấp 2: OpenTelemetry OTLP Collector Bridge
    otlp_payload = {
        "trace_name": "HTTP_GET_Knowledge",
        "metric_name": "db_query_latency",
        "metric_value": 15.4,
    }
    otlp_resp = client.post("/telemetry/otlp/export", json=otlp_payload)
    assert otlp_resp.status_code == 200
    assert otlp_resp.json()["status"] == "EXPORTED"

    # 3. Test Nâng cấp 3: Real GitHub GitOps Driver
    gitops_payload = {
        "branch_name": "feature/auto-fix-leak",
        "file_path": "capabilities/finance/config.yaml",
        "content": "status: active",
        "commit_message": "fix(auto): fix finance config leak",
        "pr_title": "[Auto-Fix] Finance Config Patch",
    }
    gitops_resp = client.post("/gitops/github/create-pr", json=gitops_payload)
    assert gitops_resp.status_code == 200
    gitops_data = gitops_resp.json()
    assert gitops_data["status"] in ["SUCCESS", "SIMULATED_GITOPS"]
    assert "github.com" in gitops_data["pr_url"]

    # 4. Test Nâng cấp 4: Dynamic Capability Hot-Swapper
    hot_plug_payload = {"pack_name": "payroll"}
    hot_resp = client.post(
        "/capabilities/hot-plug/load", json=hot_plug_payload
    )
    assert hot_resp.status_code == 200
    assert hot_resp.json()["status"] == "SUCCESS"

    # Gọi Endpoint mới được cắm nóng động trong RAM
    status_resp = client.get("/v1/payroll/status")
    assert status_resp.status_code == 200
    assert status_resp.json()["pack"] == "payroll"
