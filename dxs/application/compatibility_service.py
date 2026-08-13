from __future__ import annotations

from dxs.contracts.versioning import ContractVersion
from dxs.domain.compatibility import (
    CompatibilityPolicy,
    CompatibilityResult,
)
from dxs.ports.compatibility import CompatibilityChecker


class CompatibilityService:
    """Application service for contract compatibility evaluation."""

    def __init__(self, checker: CompatibilityChecker) -> None:
        self._checker = checker

    def check(
        self,
        current: ContractVersion,
        target: ContractVersion,
        policy: CompatibilityPolicy | None = None,
    ) -> CompatibilityResult:
        active_policy = policy or CompatibilityPolicy()

        return self._checker.check(
            current=current,
            target=target,
            policy=active_policy,
        )


__all__ = ["CompatibilityService"]
