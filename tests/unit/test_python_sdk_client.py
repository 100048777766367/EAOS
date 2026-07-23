"""Unit test suite for EAOS Python client SDK."""

from sdk.python.eaos_sdk import EAOSClientConfig, EAOSClientSDK


def test_eaos_python_sdk_client_health() -> None:
    """Verifies Python SDK health query."""
    sdk = EAOSClientSDK()
    health = sdk.get_system_health()
    assert health["status"] == "healthy"


def test_eaos_python_sdk_compile_rego() -> None:
    """Verifies Python SDK Rego policy compilation call."""
    cfg = EAOSClientConfig(gateway_url="http://localhost:8000")
    sdk = EAOSClientSDK(cfg)
    res = sdk.compile_rego_policy("allow = true", {"role": "admin"})
    assert res["passed"] is True
