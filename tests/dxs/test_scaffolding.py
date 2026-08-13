from pathlib import Path

from dxs.scaffolding.service import scaffold_capability


def test_scaffold_is_idempotent(tmp_path: Path) -> None:
    first = scaffold_capability(tmp_path, "customer_management")
    second = scaffold_capability(tmp_path, "customer_management")
    assert len(first.created) == 6
    assert len(second.created) == 0
    assert len(second.skipped) == 6
