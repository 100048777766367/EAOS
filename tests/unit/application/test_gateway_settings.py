"""Unit tests for EAOS Gateway Settings and Web Settings."""

from __future__ import annotations

import pytest
from apps.api.app.settings import api_settings
from apps.web.app.settings import web_settings


def test_gateway_settings_defaults() -> None:
    """Test default values of Gateway Settings."""
    assert api_settings.title == "EAOS API Gateway"
    assert api_settings.version == "0.1.0"


def test_web_settings_defaults() -> None:
    """Test default values of Web UI Settings."""
    assert web_settings.title == "EAOS Web UI Gateway"
    assert web_settings.version == "0.2.0"
    assert web_settings.port == 3002
    assert web_settings.host == "127.0.0.1"


def test_web_settings_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test environment variable overrides for Web UI Settings."""
    monkeypatch.setenv("EAOS_WEB_PORT", "3005")
    monkeypatch.setenv("EAOS_WEB_DEBUG", "true")

    from apps.web.app.settings import WebSettings

    custom_settings = WebSettings()
    assert custom_settings.port == 3005
    assert custom_settings.debug is True
