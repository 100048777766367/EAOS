import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_reflection_engine_diagnosis_flow(client: TestClient) -> None:
    # Mô phỏng kịch bản: Gặp lỗi kiểm định Fitness ranh giới
    payload = {
        "subject_id": "EVO-ILLEGAL-BOUNDARY-MOD",
        "trigger_event": "Fitness Validation Failure",
        "passed_checks": False,
    }

    # Kích hoạt Reflection Engine tự chẩn đoán nguyên nhân
    response = client.post("/reflection/analyze", json=payload)
    assert response.status_code == 201

    report = response.json()
    assert report["id"].startswith("REF-")
    assert report["subject"] == payload["subject_id"]
    assert report["confidence"] == 0.95

    # Đảm bảo Reflection tự động tìm ra Root Cause chính xác
    assert len(report["root_causes"]) == 1
    root_cause = report["root_causes"][0]
    assert root_cause["type"] == "BoundaryViolation"
    assert "import sai lớp phân tách" in root_cause["description"]

    # Đảm bảo sinh ra khuyến nghị hành động mức ưu tiên HIGH
    assert len(report["recommendations"]) == 1
    recommendation = report["recommendations"][0]
    assert recommendation["priority"] == "HIGH"
    assert "ranh giới dependencies" in recommendation["action"]