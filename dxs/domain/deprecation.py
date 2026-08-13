from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from dxs.contracts.versioning import ContractVersion


class DeprecationStatus(StrEnum):
    """Lifecycle status of a deprecated contract version."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    RETIRED = "retired"


@dataclass(frozen=True, slots=True)
class DeprecationRecord:
    """Immutable deprecation metadata."""

    contract_name: str
    version: ContractVersion
    status: DeprecationStatus
    replacement: ContractVersion | None = None
    reason: str = ""

    def __post_init__(self) -> None:
        name = self.contract_name.strip()

        if not name:
            raise ValueError("Contract name cannot be empty.")

        if self.status is DeprecationStatus.DEPRECATED and not self.reason.strip():
            raise ValueError("Deprecated contracts require a deprecation reason.")

        object.__setattr__(self, "contract_name", name)


class DeprecationPolicy:
    """Deterministic policy for contract deprecation state."""

    def __init__(
        self,
        records: tuple[DeprecationRecord, ...] = (),
    ) -> None:
        self._records = records

    def status(
        self,
        contract_name: str,
        version: ContractVersion,
    ) -> DeprecationStatus:
        """Return the known status or ACTIVE when no record exists."""

        name = contract_name.strip()

        for record in self._records:
            if record.contract_name == name and record.version == version:
                return record.status

        return DeprecationStatus.ACTIVE

    def is_deprecated(
        self,
        contract_name: str,
        version: ContractVersion,
    ) -> bool:
        """Return whether the specified version is deprecated."""

        return (
            self.status(
                contract_name,
                version,
            )
            is DeprecationStatus.DEPRECATED
        )

    def is_retired(
        self,
        contract_name: str,
        version: ContractVersion,
    ) -> bool:
        """Return whether the specified version is retired."""

        return (
            self.status(
                contract_name,
                version,
            )
            is DeprecationStatus.RETIRED
        )

    def records(self) -> tuple[DeprecationRecord, ...]:
        """Return records in deterministic order."""

        return tuple(
            sorted(
                self._records,
                key=lambda item: (
                    item.contract_name,
                    item.version,
                ),
            )
        )


__all__ = [
    "DeprecationPolicy",
    "DeprecationRecord",
    "DeprecationStatus",
]
