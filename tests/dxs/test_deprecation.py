from dxs.contracts.versioning import ContractVersion
from dxs.domain.deprecation import (
    DeprecationPolicy,
    DeprecationRecord,
    DeprecationStatus,
)


def test_unknown_version_is_active() -> None:
    policy = DeprecationPolicy()

    assert (
        policy.status(
            "repository",
            ContractVersion(1, 0, 0),
        )
        is DeprecationStatus.ACTIVE
    )


def test_deprecated_version_is_detected() -> None:
    record = DeprecationRecord(
        contract_name="repository",
        version=ContractVersion(1, 0, 0),
        status=DeprecationStatus.DEPRECATED,
        replacement=ContractVersion(1, 1, 0),
        reason="Superseded by the next contract version.",
    )

    policy = DeprecationPolicy(records=(record,))

    assert policy.is_deprecated(
        "repository",
        ContractVersion(1, 0, 0),
    )
    assert (
        policy.is_retired(
            "repository",
            ContractVersion(1, 0, 0),
        )
        is False
    )
