from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DebugResult:
    name: str
    passed: bool
    message: str

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.name}: {self.message}"


class DebuggingService:
    """Run deterministic, non-mutating repository diagnostics."""

    def inspect(self, root: Path) -> list[DebugResult]:
        results: list[DebugResult] = []

        results.append(self._check_root(root))
        results.append(self._check_dxs(root))
        results.append(self._check_tests(root))

        return results

    @staticmethod
    def _check_root(root: Path) -> DebugResult:
        passed = root.exists() and root.is_dir()

        return DebugResult(
            name="repository_root",
            passed=passed,
            message=str(root),
        )

    @staticmethod
    def _check_dxs(root: Path) -> DebugResult:
        path = root / "dxs"
        passed = path.exists() and path.is_dir()

        return DebugResult(
            name="dxs_directory",
            passed=passed,
            message=str(path),
        )

    @staticmethod
    def _check_tests(root: Path) -> DebugResult:
        path = root / "tests" / "dxs"
        passed = path.exists() and path.is_dir()

        return DebugResult(
            name="dxs_tests",
            passed=passed,
            message=str(path),
        )
