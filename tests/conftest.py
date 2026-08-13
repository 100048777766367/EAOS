"""Master Pytest Fixtures for EAOS Test Suite."""

import sys
from collections.abc import Generator
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from apps.api.app.main import app as api_app  # noqa: E402
from apps.web.app.main import app as web_app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture
def api_client() -> Generator[TestClient]:
    """Provides a TestClient instance for the EAOS API Gateway."""
    with TestClient(api_app) as client:
        yield client


@pytest.fixture
def web_client() -> Generator[TestClient]:
    """Provides a TestClient instance for the EAOS Web UI."""
    with TestClient(web_app) as client:
        yield client


@pytest.fixture
def client(api_client: TestClient) -> TestClient:
    """Alias fixture providing TestClient for API Gateway."""
    return api_client
