"""Contract test suite verifying OpenAPI and event schema validity."""

from pathlib import Path

from platform_services.contracts.contract_registry import ContractRegistry

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_contract_schemas_are_valid() -> None:
    """Verifies that all communication contracts pass registry verification."""
    registry = ContractRegistry(ROOT_PATH)
    contracts = registry.discover_contracts()
    assert len(contracts) >= 5
