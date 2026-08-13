from dxs.contracts.evolution import (
    ContractFamily,
    ContractLifecycle,
    VersionedContract,
)
from dxs.contracts.versioning import ContractVersion


def test_versioned_contract_has_stable_identifier() -> None:
    contract = VersionedContract(
        name="repository",
        version=ContractVersion(1, 0, 0),
    )

    assert contract.identifier == "repository@1.0.0"
    assert contract.active is True


def test_contract_family_returns_active_versions_sorted() -> None:
    family = ContractFamily(
        name="repository",
        versions=(
            VersionedContract(
                "repository",
                ContractVersion(1, 1, 0),
            ),
            VersionedContract(
                "repository",
                ContractVersion(1, 0, 0),
                ContractLifecycle.DEPRECATED,
            ),
        ),
    )

    assert [str(item.version) for item in family.active_versions] == ["1.1.0"]
