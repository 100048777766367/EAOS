from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from dxs.contracts.versioning import ContractVersion


class MigrationAction(StrEnum):
    """Action required for a contract migration."""

    NOOP = "noop"
    MIGRATE = "migrate"
    BLOCK = "block"


@dataclass(frozen=True, slots=True)
class MigrationStep:
    """One immutable migration step."""

    source: ContractVersion
    target: ContractVersion
    action: MigrationAction
    reason: str


@dataclass(frozen=True, slots=True)
class MigrationPlan:
    """Immutable migration plan containing ordered steps."""

    current: ContractVersion
    target: ContractVersion
    steps: tuple[MigrationStep, ...]

    @property
    def executable(self) -> bool:
        """Return whether the plan contains no blocked steps."""

        return all(step.action is not MigrationAction.BLOCK for step in self.steps)


class MigrationPlanner:
    """Deterministic migration planner with no repository mutation."""

    def plan(
        self,
        current: ContractVersion,
        target: ContractVersion,
        compatible: bool,
    ) -> MigrationPlan:
        """Create a migration plan without executing any change."""

        if current == target:
            step = MigrationStep(
                source=current,
                target=target,
                action=MigrationAction.NOOP,
                reason="Current and target versions are identical.",
            )
        elif not compatible:
            step = MigrationStep(
                source=current,
                target=target,
                action=MigrationAction.BLOCK,
                reason="Migration is blocked because versions are incompatible.",
            )
        else:
            step = MigrationStep(
                source=current,
                target=target,
                action=MigrationAction.MIGRATE,
                reason="Migration is eligible under the active policy.",
            )

        return MigrationPlan(
            current=current,
            target=target,
            steps=(step,),
        )


__all__ = [
    "MigrationAction",
    "MigrationPlan",
    "MigrationPlanner",
    "MigrationStep",
]
