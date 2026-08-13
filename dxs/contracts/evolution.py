from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from dxs.contracts.versioning import ContractVersion


class ContractLifecycle(StrEnum):
    """Lifecycle state of a versioned contract."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    RETIRED = "retired"


@dataclass(frozen=True, slots=True)
class VersionedContract:
    """Immutable identity and lifecycle metadata for a contract."""

    name: str
    version: ContractVersion
    lifecycle: ContractLifecycle = ContractLifecycle.ACTIVE

    def __post_init__(self) -> None:
        normalized = self.name.strip()

        if not normalized:
            raise ValueError("Contract name cannot be empty.")

        object.__setattr__(self, "name", normalized)

    @property
    def identifier(self) -> str:
        """Return the stable contract identifier."""

        return f"{self.name}@{self.version}"

    @property
    def active(self) -> bool:
        """Return whether the contract is active."""

        return self.lifecycle is ContractLifecycle.ACTIVE


@dataclass(frozen=True, slots=True)
class ContractFamily:
    """Immutable collection of versions belonging to one contract."""

    name: str
    versions: tuple[VersionedContract, ...]

    def __post_init__(self) -> None:
        normalized = self.name.strip()

        if not normalized:
            raise ValueError("Contract family name cannot be empty.")

        if not self.versions:
            raise ValueError("Contract family must contain at least one version.")

        if any(item.name != normalized for item in self.versions):
            raise ValueError("All versions must belong to the same contract family.")

        object.__setattr__(self, "name", normalized)

    @property
    def active_versions(self) -> tuple[VersionedContract, ...]:
        """Return active versions in deterministic version order."""

        return tuple(
            sorted(
                (item for item in self.versions if item.lifecycle is ContractLifecycle.ACTIVE),
                key=lambda item: item.version,
            )
        )


__all__ = [
    "ContractFamily",
    "ContractLifecycle",
    "VersionedContract",
]
