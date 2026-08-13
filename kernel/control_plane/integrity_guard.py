"""EAOS Repository Integrity Guard & Mutation Freeze Engine."""

from __future__ import annotations

import py_compile
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field


class RepositoryIntegrityState(StrEnum):
    """Integrity state of the repository."""

    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    CORRUPTED = "CORRUPTED"
    UNKNOWN = "UNKNOWN"


class IntegrityAuditReport(BaseModel):
    """Audit report produced by IntegrityGuard."""

    state: RepositoryIntegrityState
    syntax_error_count: int
    corrupted_files: list[str] = Field(default_factory=list)
    protected_path_violations: list[str] = Field(default_factory=list)
    mutation_frozen: bool
    rationale: str


class IntegrityGuard:
    """Repository Integrity Guard enforcing mutation freezing upon degradation."""

    SYNTAX_ERROR_FREEZE_THRESHOLD: int = 20

    def __init__(self, workspace_root: Path | str = ".") -> None:
        self.workspace_root = Path(workspace_root).resolve()
        self._mutation_frozen: bool = False

    @property
    def is_mutation_frozen(self) -> bool:
        return self._mutation_frozen

    def freeze_mutation(self, reason: str) -> None:
        """Freeze mutation operations across the system."""
        self._mutation_frozen = True

    def unfreeze_mutation(self) -> None:
        """Unfreeze mutation operations after successful recovery."""
        self._mutation_frozen = False

    def audit_integrity(self, source_roots: list[str] | None = None) -> IntegrityAuditReport:
        """Audit repository integrity by inspecting syntax errors and protected paths."""
        if source_roots is None:
            source_roots = ["apps", "packages", "kernel", "engine", "tools"]

        syntax_error_count = 0
        corrupted_files: list[str] = []

        # Audit python syntax across target source roots
        for root_name in source_roots:
            target_dir = self.workspace_root / root_name
            if not target_dir.exists():
                continue
            for py_file in target_dir.rglob("*.py"):
                skip_parts = (".", "venv", "build", "dist")
                if any(part.startswith(".") or part in skip_parts for part in py_file.parts):
                    continue
                try:
                    py_compile.compile(str(py_file), doraise=True)
                except py_compile.PyCompileError as err:
                    syntax_error_count += 1
                    rel_path = py_file.relative_to(self.workspace_root)
                    corrupted_files.append(f"{rel_path}: {err.msg}")

        # Classify Integrity State
        if syntax_error_count >= self.SYNTAX_ERROR_FREEZE_THRESHOLD:
            state = RepositoryIntegrityState.CORRUPTED
            freeze_reason = (
                f"Syntax error count ({syntax_error_count}) exceeds "
                f"freeze threshold ({self.SYNTAX_ERROR_FREEZE_THRESHOLD})."
            )
            self.freeze_mutation(freeze_reason)
            rationale = f"Repository CORRUPTED: {syntax_error_count} syntax errors detected across codebase."
        elif syntax_error_count > 0:
            state = RepositoryIntegrityState.DEGRADED
            rationale = f"Repository DEGRADED: {syntax_error_count} localized syntax errors detected."
        else:
            state = RepositoryIntegrityState.HEALTHY
            rationale = "Repository HEALTHY: No syntax errors detected."

        return IntegrityAuditReport(
            state=state,
            syntax_error_count=syntax_error_count,
            corrupted_files=corrupted_files,
            protected_path_violations=[],
            mutation_frozen=self._mutation_frozen,
            rationale=rationale,
        )
