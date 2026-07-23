"""Performance test suite verifying sub-50ms latency SLAs."""

import time

from apps.api.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_performance_health_endpoint_latency_sla() -> None:
    """Verifies that health check endpoint responds in under 50ms."""
    # Execute warm-up request to prime FastAPI framework caching
    client.get("/health")

    latencies: list[float] = []
    for _ in range(5):
        start_time = time.perf_counter()
        response = client.get("/health")
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        assert response.status_code == 200
        latencies.append(elapsed_ms)

    latencies.sort()
    median_latency = latencies[len(latencies) // 2]
    assert median_latency < 50.0
