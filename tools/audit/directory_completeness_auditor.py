"""Directory Completeness Auditor for EAOS Monorepo.

Validates that zero empty or hollow directories exist and analyzes directory splitting conflicts.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Final

from pydantic import BaseModel, Field

DEFAULT_IGNORED_DIRS: Final[set[str]] = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "build",
    "dist",
    "node_modules",
    ".idea",
    ".vscode",
}


class ViolationType(Enum):
    """Classification of directory completeness violations."""

    COMPLETELY_EMPTY = auto()
    HOLLOW_DIRECTORY = auto()


class DirectoryViolation(BaseModel):
    """Structured representation of a directory completeness violation."""

    path: str = Field(description="Relative path of the violating directory")
    violation_type: ViolationType = Field(description="Type of violation detected")
    details: str = Field(description="Contextual explanation of the violation")


class DirectoryConflict(BaseModel):
    """Represents a structural or boundary splitting conflict within the directory tree."""

    path: str = Field(description="Relative path of the conflicting directory")
    conflict_type: str = Field(default="UNINDEXED_PACKAGE_SPLIT", description="Type of split conflict detected")
    description: str = Field(default="", description="Contextual description of the conflict")
    recommended_strategy: str = Field(default="INDEX_OR_CONSOLIDATE", description="Recommended resolution strategy")
    strategy: str = Field(default="INDEX_OR_CONSOLIDATE", description="Alias strategy recommendation")

    def __getitem__(self, item: str) -> Any:
        """Allow dict-like item access for backwards compatibility with tests."""
        return getattr(self, item)


@dataclass(slots=True)
class AuditReport:
    """Audit summary report payload."""

    total_directories_scanned: int = 0
    violations: list[DirectoryViolation] = field(default_factory=list)
    conflicts: list[DirectoryConflict] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        """Return True if no completeness violations or conflicts were discovered."""
        return len(self.violations) == 0 and len(self.conflicts) == 0

    @property
    def completely_empty_count(self) -> int:
        """Count of directories with 0 subdirectories and 0 files."""
        return sum(1 for v in self.violations if v.violation_type == ViolationType.COMPLETELY_EMPTY)

    @property
    def hollow_count(self) -> int:
        """Count of directories with subdirectories but zero files in entire subtree."""
        return sum(1 for v in self.violations if v.violation_type == ViolationType.HOLLOW_DIRECTORY)


class DirectoryCompletenessAuditor:
    """Engine responsible for inspecting monorepo structural integrity and split conflicts."""

    def __init__(
        self,
        root_path: Path | str,
        ignored_dirs: set[str] | None = None,
    ) -> None:
        self.root_path: Path = Path(root_path).resolve()
        self.ignored_dirs: set[str] = ignored_dirs if ignored_dirs is not None else DEFAULT_IGNORED_DIRS

    def _should_ignore(self, path: Path) -> bool:
        """Determine whether a given path should be bypassed during auditing."""
        return any(part in self.ignored_dirs for part in path.parts)

    def scan_empty_directories(self) -> list[Path]:
        """Scan for completely empty directories (0 files and 0 subdirectories)."""
        empty_dirs: list[Path] = []
        for path in self.root_path.rglob("*"):
            if path.is_dir() and not self._should_ignore(path):
                try:
                    next(path.iterdir())
                except StopIteration:
                    empty_dirs.append(path)
                except PermissionError:
                    continue
        return empty_dirs

    def scan_hollow_directories(self) -> list[Path]:
        """Scan for hollow directories (contains child folders but zero files across hierarchy)."""
        hollow_dirs: list[Path] = []
        for path in self.root_path.rglob("*"):
            if path.is_dir() and not self._should_ignore(path):
                try:
                    has_children = any(True for _ in path.iterdir())
                except PermissionError:
                    continue

                if has_children:
                    has_files = any(p.is_file() for p in path.rglob("*") if not self._should_ignore(p))
                    if not has_files:
                        hollow_dirs.append(path)
        return hollow_dirs

    def analyze_splitting_conflicts(self) -> list[DirectoryConflict]:
        """Analyze boundary and directory splitting conflicts across monorepo layers.

        Identifies structural split anomalies where subpackages exist without parent
        package index files or where conflicting bounded context splits exist.
        """
        conflicts: list[DirectoryConflict] = []
        for path in self.root_path.rglob("*"):
            if path.is_dir() and not self._should_ignore(path):
                rel_path = str(path.relative_to(self.root_path))
                try:
                    child_dirs = [p for p in path.iterdir() if p.is_dir() and not self._should_ignore(p)]
                except PermissionError:
                    continue

                if child_dirs:
                    # Check if subdirectories contain Python code while parent is missing __init__.py
                    has_sub_py = any(p.suffix == ".py" for p in path.rglob("*.py") if not self._should_ignore(p))
                    has_parent_init = (path / "__init__.py").exists()

                    if has_sub_py and not has_parent_init:
                        conflicts.append(
                            DirectoryConflict(
                                path=rel_path,
                                conflict_type="UNINDEXED_PACKAGE_SPLIT",
                                description=(
                                    f"Directory '{rel_path}' has split sub-packages with Python code "
                                    "but lacks an explicit parent __init__.py package index."
                                ),
                                recommended_strategy="ADD_PACKAGE_INDEX",
                                strategy="ADD_PACKAGE_INDEX",
                            )
                        )
        return conflicts

    def execute_audit(self) -> AuditReport:
        """Run complete monorepo directory completeness and split conflict audit."""
        report = AuditReport()
        scanned_count = 0

        for path in self.root_path.rglob("*"):
            if path.is_dir() and not self._should_ignore(path):
                scanned_count += 1
                rel_path = str(path.relative_to(self.root_path))

                try:
                    contents = list(path.iterdir())
                except PermissionError:
                    continue

                if not contents:
                    report.violations.append(
                        DirectoryViolation(
                            path=rel_path,
                            violation_type=ViolationType.COMPLETELY_EMPTY,
                            details="Directory contains 0 files and 0 subdirectories.",
                        )
                    )
                    continue

                has_files = any(p.is_file() for p in path.rglob("*") if not self._should_ignore(p))
                if not has_files:
                    report.violations.append(
                        DirectoryViolation(
                            path=rel_path,
                            violation_type=ViolationType.HOLLOW_DIRECTORY,
                            details="Directory contains subfolders but zero files.",
                        )
                    )

        report.conflicts = self.analyze_splitting_conflicts()
        report.total_directories_scanned = scanned_count
        return report


def main(argv: Sequence[str] | None = None) -> int:
    """CLI Entry point for DirectoryCompletenessAuditor."""
    parser = argparse.ArgumentParser(description="Audit monorepo for empty/hollow directories and splitting conflicts.")
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Root directory to scan (default: current working directory)",
    )
    args = parser.parse_args(argv)

    auditor = DirectoryCompletenessAuditor(root_path=args.root)
    report = auditor.execute_audit()

    print("=" * 80)
    print(" EAOS MONOREPO DIRECTORY AUDIT SUMMARY")
    print("=" * 80)
    print(f" Total Directories Scanned : {report.total_directories_scanned}")
    print(f" Completely Empty Count    : {report.completely_empty_count}")
    print(f" Hollow Directories Count   : {report.hollow_count}")
    print(f" Splitting Conflicts Count : {len(report.conflicts)}")
    print("=" * 80)

    if not report.is_clean:
        if report.violations:
            print("\nVIOLATIONS DETECTED:")
            for violation in report.violations:
                print(f" - [{violation.violation_type.name}] {violation.path}: {violation.details}")
        if report.conflicts:
            print("\nSPLITTING CONFLICTS DETECTED:")
            for conflict in report.conflicts:
                print(f" - [{conflict.conflict_type}] {conflict.path}: {conflict.description}")
        return 1

    print("\nAUDIT SUCCESSFUL: Zero violations and zero splitting conflicts detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
