import pytest


@pytest.fixture(autouse=True)
def setup_test_environment() -> None:
    """Fixture tự động thiết lập môi trường test."""
