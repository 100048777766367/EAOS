from __future__ import annotations

from typing import Protocol

from dxs.contracts.versioning import ContractVersion
from dxs.domain.compatibility import (
    CompatibilityPolicy,
    CompatibilityResult,
)


class CompatibilityChecker(Protocol):
    """Port for contract compatibility evaluation."""

    def check(
        self,
        current: ContractVersion,
        target: ContractVersion,
        policy: CompatibilityPolicy,
    ) -> CompatibilityResult: ...
