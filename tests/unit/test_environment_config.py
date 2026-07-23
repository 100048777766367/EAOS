"""Unit test suite for EAOS environment configuration loader."""

from pathlib import Path

from platform_services.config.environment_config import (
    EnvironmentConfigLoader,
    SystemEnvironment,
)

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_config_loader_development() -> None:
    """Verifies loading development environment settings."""
    loader = EnvironmentConfigLoader(ROOT_PATH)
    settings = loader.load_settings("development")
    assert settings.environment == SystemEnvironment.DEVELOPMENT
    assert settings.debug is True
    assert "postgresql" in settings.database.url


def test_config_loader_production() -> None:
    """Verifies loading production environment settings."""
    loader = EnvironmentConfigLoader(ROOT_PATH)
    settings = loader.load_settings("production")
    assert settings.environment == SystemEnvironment.PRODUCTION
    assert settings.debug is False
    assert "eaos_db" in settings.database.url
