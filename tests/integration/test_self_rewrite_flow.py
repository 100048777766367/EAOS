import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_agent_chain_self_rewrite_flow(client: TestClient) -> None:
    # 1. Thiết lập bài toán sự cố DB cần giải quyết
    payload = {
        "problem": "Database port mismatch causing connection timeouts.",
        "author": "SystemMonitor",
    }

    # 2. Kích hoạt Self Rewrite Engine
    response = client.post("/self-rewrite/run", json=payload)
    assert response.status_code == 201

    job = response.json()
    assert job["id"].startswith("REW-")
    assert job["status"] == "SUCCESS"

    # Kiểm chứng chuỗi 5 AI Agents cốt lõi đã thực thi đầy đủ
    logs = job["agent_logs"]
    assert len(logs) == 5
    assert logs[0]["agent_role"] == "Planner"
    assert logs[2]["agent_role"] == "Coder"
    assert logs[4]["agent_role"] == "Tester"

    # Kiểm chứng Pull Request đề xuất chứa file patch/diff chính xác
    pr = job["pull_request"]
    assert pr["id"].startswith("PR-")
    assert "Fix Database Port Parameter" in pr["title"]
    assert pr["target_branch"] == "main"
    assert len(pr["patches"]) == 1
    assert "db_port = 5433" in pr["patches"][0]["diff_content"]