from __future__ import annotations

from dxs.contracts.versioning import ContractVersion
from dxs.domain.compatibility import (
    CompatibilityPolicy,
    CompatibilityResult,
)


class CompatibilityAdapter:
    """Default in-process compatibility checker."""

    def check(
        self,
        current: ContractVersion,
        target: ContractVersion,
        policy: CompatibilityPolicy,
    ) -> CompatibilityResult:
        compatible = policy.is_compatible(
            current=current,
            target=target,
        )

        if compatible:
            reason = f"Contract versions {current} and {target} are compatible under the active policy."
        else:
            reason = f"Contract versions {current} and {target} are incompatible under the active policy."

        return CompatibilityResult(
            compatible=compatible,
            current_version=current,
            target_version=target,
            reason=reason,
            policy=policy,
        )


__all__ = ["CompatibilityAdapter"]
