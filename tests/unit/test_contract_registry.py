"""Unit test suite for EAOS communication contract registry."""

from pathlib import Path

from platform_services.contracts.contract_registry import ContractRegistry

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_contract_registry_discovers_all_protocols() -> None:
    """Verifies that contract registry discovers schemas across 5 protocols."""
    registry = ContractRegistry(ROOT_PATH)
    contracts = registry.discover_contracts()
    assert len(contracts) >= 5
    types = [c.protocol_type for m in contracts for c in [m]]
    assert "ASYNC_EVENT_SCHEMA" in types
    assert "GRAPHQL_SCHEMA" in types
    assert "GRPC_PROTOBUF" in types
    assert "MODEL_CONTEXT_PROTOCOL" in types
    assert "OPENAPI_SPEC" in types
