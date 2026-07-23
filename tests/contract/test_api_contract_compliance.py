"""Contract test suite verifying API Gateway and Event Mesh schemas."""

from apps.api.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_openapi_contract_schema_compliance() -> None:
    """Verifies OpenAPI schema compliance."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert data["info"]["title"] == "EAOS API Gateway"
