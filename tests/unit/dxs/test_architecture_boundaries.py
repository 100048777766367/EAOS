from __future__ import annotations

from pathlib import Path

from dxs.application.architecture_checker import ArchitectureChecker


def run_checker() -> ArchitectureChecker:
    root = Path(__file__).resolve().parents[3] / "dxs"

    checker = ArchitectureChecker(root)
    checker.run()

    return checker


def test_dxs_architecture_has_no_violations() -> None:
    checker = run_checker()

    failures = [result for result in checker.results if not result.passed]

    assert not failures, "\n".join((f"{result.rule_id}: {result.message}") for result in failures)
