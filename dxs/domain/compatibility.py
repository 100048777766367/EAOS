from __future__ import annotations

from dataclasses import dataclass

from dxs.contracts.versioning import ContractVersion


@dataclass(frozen=True, slots=True)
class CompatibilityPolicy:
    """Defines compatibility rules between contract versions."""

    allow_minor_upgrade: bool = True
    allow_patch_upgrade: bool = True

    def is_compatible(
        self,
        current: ContractVersion,
        target: ContractVersion,
    ) -> bool:
        """Return whether two contract versions are compatible."""

        if current.major != target.major:
            return False

        if current == target:
            return True

        if target.minor < current.minor:
            return False

        if target.minor == current.minor:
            return self.allow_patch_upgrade

        return self.allow_minor_upgrade


@dataclass(frozen=True, slots=True)
class CompatibilityResult:
    """Structured result of a contract compatibility evaluation."""

    compatible: bool
    current_version: ContractVersion
    target_version: ContractVersion
    reason: str
    policy: CompatibilityPolicy

    @property
    def status(self) -> str:
        return "compatible" if self.compatible else "incompatible"
