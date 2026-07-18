import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_reflection_to_learning_ingestion_flow(client: TestClient) -> None:
    # 1. Tạo một báo cáo Reflection chẩn đoán sự cố (Thất bại)
    reflection_payload = {
        "subject_id": "EVO-ILLEGAL-BOUNDARY-MOD",
        "trigger_event": "Fitness Validation Failure",
        "passed_checks": False,
    }
    ref_response = client.post("/reflection/analyze", json=reflection_payload)
    assert ref_response.status_code == 201
    ref_report = ref_response.json()
    ref_id = ref_report["id"]

    # 2. Kích hoạt Learning Engine để nạp vết sự cố thành Kinh nghiệm thực tế
    ingest_payload = {"reflection_id": ref_id}
    learn_response = client.post("/learning/ingest", json=ingest_payload)
    assert learn_response.status_code == 201

    experience = learn_response.json()
    assert experience["id"].startswith("EXP-")
    assert experience["reflection_id"] == ref_id
    assert "Kinh nghiệm từ sự cố" in experience["title"]

    # Đảm bảo tri thức được đúc rút đầy đủ Lessons, Patterns, Anti-Patterns
    assert len(experience["lessons"]) == 1
    assert experience["lessons"][0]["id"] == "L-01"
    assert "Ports & Adapters" in experience["lessons"][0]["action_item"]

    assert len(experience["anti_patterns"]) == 1
    assert "Database Leak" in experience["anti_patterns"][0]["name"]

    assert len(experience["heuristics"]) == 1
    assert "H-01" in experience["heuristics"][0]["id"]