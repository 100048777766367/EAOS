import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_proposal_simulation_dry_run_flow(client: TestClient) -> None:
    # 1. Thiết lập kịch bản mô phỏng đề xuất thay đổi cấu hình hợp lệ
    payload = {
        "scenario_id": "SCEN-EVO-AGENT-01",
        "scenario_name": "Propose LLM Temperature Change",
        "description": "Giảm độ sáng tạo để tăng tính chính xác của Coder Agent",
        "target_payload": {
            "temperature": 0.2,
            "max_tokens": 4096,
            "__version": 3,  # Hợp chuẩn hiến pháp
        },
    }

    # 2. Khởi chạy Simulation Engine trên Sandbox cô lập
    response = client.post("/simulation/run", json=payload)
    assert response.status_code == 201

    simulation = response.json()
    assert simulation["id"].startswith("SIM-")
    assert simulation["status"] == "SUCCESS"

    # Kiểm chứng kết quả chạy khô Dry-run 1000 tests giả lập đạt chuẩn
    result = simulation["result"]
    assert result["passed_tests_count"] == 1000
    assert result["failed_tests_count"] == 0
    assert result["simulated_fitness_score"] == 1.0
    assert result["policy_passed"] is True

    # Kiểm chứng dự báo hiệu năng tính toán tối ưu
    metrics = result["metrics"]
    assert metrics["estimated_latency_ms"] == 120.5
    assert metrics["expected_cpu_usage"] == 15.4
    assert metrics["simulated_memory_mb"] == 128.0