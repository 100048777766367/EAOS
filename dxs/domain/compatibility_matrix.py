from __future__ import annotations

from dataclasses import dataclass

from dxs.contracts.versioning import ContractVersion
from dxs.domain.compatibility import CompatibilityPolicy


@dataclass(frozen=True, slots=True)
class CompatibilityMatrixCell:
    """One deterministic compatibility matrix entry."""

    current: ContractVersion
    target: ContractVersion
    compatible: bool
    reason: str


class CompatibilityMatrix:
    """Deterministic matrix for pairwise contract compatibility."""

    def __init__(
        self,
        policy: CompatibilityPolicy | None = None,
    ) -> None:
        self.policy = policy or CompatibilityPolicy()

    def evaluate(
        self,
        current_versions: tuple[ContractVersion, ...],
        target_versions: tuple[ContractVersion, ...],
    ) -> tuple[CompatibilityMatrixCell, ...]:
        """Evaluate every current/target pair deterministically."""

        cells: list[CompatibilityMatrixCell] = []

        for current in sorted(current_versions):
            for target in sorted(target_versions):
                compatible = self.policy.is_compatible(
                    current=current,
                    target=target,
                )

                if compatible:
                    reason = "Compatible under the active policy."
                else:
                    reason = "Incompatible under the active policy."

                cells.append(
                    CompatibilityMatrixCell(
                        current=current,
                        target=target,
                        compatible=compatible,
                        reason=reason,
                    )
                )

        return tuple(cells)

    def is_compatible(
        self,
        current: ContractVersion,
        target: ContractVersion,
    ) -> bool:
        """Return compatibility for one version pair."""

        return self.policy.is_compatible(
            current=current,
            target=target,
        )


__all__ = [
    "CompatibilityMatrix",
    "CompatibilityMatrixCell",
]
