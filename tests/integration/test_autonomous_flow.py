import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_infinite_evolution_autonomous_loop_flow(client: TestClient) -> None:
    # 1. Kích hoạt toàn bộ vòng lặp tự trị tiến hóa đóng kín
    payload = {
        "problem": "System latency exceeded threshold, trigger self-heal",
        "author": "MonitorDaemon",
    }

    response = client.post("/autonomous/run-cycle", json=payload)
    assert response.status_code == 201

    cycle = response.json()
    assert cycle["cycle_id"].startswith("CYC-")
    assert cycle["status"] == "SUCCESS"

    # Kiểm chứng đầy đủ 9 mắt xích của vòng nhận thức đóng kín được ghi nhận
    stages = cycle["stage_executions"]
    assert "Observe" in stages
    assert "Reflect" in stages
    assert "Learn" in stages
    assert "Predict" in stages
    assert "Simulate" in stages
    assert "Rewrite" in stages
    assert "Council" in stages
    assert "Approve" in stages
    assert "Deploy" in stages

    assert stages["Observe"].startswith("API Response")
    assert stages["Reflect"].startswith("REF-")
    assert stages["Learn"].startswith("EXP-")
    assert stages["Approve"].startswith("TX-EVO-")
    assert "APPROVED" in stages["Council"]
    assert "Rollout" in stages["Deploy"]