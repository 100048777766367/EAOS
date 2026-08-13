from dxs.contracts.versioning import ContractVersion
from dxs.domain.migration_plan import (
    MigrationAction,
    MigrationPlanner,
)


def test_equal_versions_produce_noop() -> None:
    version = ContractVersion(1, 0, 0)

    plan = MigrationPlanner().plan(
        current=version,
        target=version,
        compatible=True,
    )

    assert plan.executable is True
    assert plan.steps[0].action is MigrationAction.NOOP


def test_compatible_versions_produce_migration() -> None:
    plan = MigrationPlanner().plan(
        current=ContractVersion(1, 0, 0),
        target=ContractVersion(1, 1, 0),
        compatible=True,
    )

    assert plan.executable is True
    assert plan.steps[0].action is MigrationAction.MIGRATE


def test_incompatible_versions_are_blocked() -> None:
    plan = MigrationPlanner().plan(
        current=ContractVersion(1, 0, 0),
        target=ContractVersion(2, 0, 0),
        compatible=False,
    )

    assert plan.executable is False
    assert plan.steps[0].action is MigrationAction.BLOCK
