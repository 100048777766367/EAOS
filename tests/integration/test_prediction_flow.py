from datetime import UTC, datetime, timedelta

import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_historical_metrics_prediction_flow(client: TestClient) -> None:
    # 1. Chuẩn bị dữ liệu lịch sử sụt giảm (Độ trễ API tăng vọt qua các ngày)
    now = datetime.now(UTC)
    payload = {
        "metric_name": "API Response Latency (ms)",
        "datapoints": [
            {"timestamp": (now - timedelta(days=3)).isoformat(), "value": 100.0},
            {"timestamp": (now - timedelta(days=2)).isoformat(), "value": 180.0},
            {"timestamp": (now - timedelta(days=1)).isoformat(), "value": 290.0},
            {"timestamp": now.isoformat(), "value": 410.0},
        ],
    }

    # 2. Gửi yêu cầu lên Prediction Engine để chẩn đoán xu hướng tương lai
    response = client.post("/prediction/run", json=payload)
    assert response.status_code == 201

    prediction = response.json()
    assert prediction["id"].startswith("PRD-")

    # Xác minh động cơ chẩn đoán chính xác xu hướng suy thoái "DEGRADING"
    assert len(prediction["trends"]) == 1
    trend = prediction["trends"][0]
    assert trend["metric_name"] == payload["metric_name"]
    assert trend["direction"] == "DEGRADING"
    assert trend["slope"] > 0  # Độ dốc hướng lên (độ trễ tăng)

    # Xác minh hệ thống tự phát đi cảnh báo rủi ro mức độ HIGH trong 90 ngày
    assert len(prediction["risks"]) == 1
    risk = prediction["risks"][0]
    assert "sụt giảm chất lượng" in risk["title"]
    assert risk["probability"] == 0.85
    assert risk["severity"] == "HIGH"