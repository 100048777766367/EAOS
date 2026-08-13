"""Workspace context manager."""

from __future__ import annotations

from pathlib import Path
from typing import Final


class ContextManager:
    """Safely read workspace files for LLM context."""

    def __init__(self, project_root: Path) -> None:
        """Initialize the workspace root."""
        self.project_root: Final[Path] = project_root.resolve()

    def _resolve_safe_path(self, relative_path: str) -> Path | None:
        """Resolve a path while enforcing the workspace boundary."""
        try:
            candidate = (self.project_root / relative_path.lstrip("/\\")).resolve()

            candidate.relative_to(self.project_root)
            return candidate

        except (OSError, ValueError):
            return None

    def build_file_context(self, relative_path: str) -> str:
        """Read a workspace file into an LLM context block."""
        if not relative_path.strip():
            return ""

        target = self._resolve_safe_path(relative_path)

        if target is None:
            return "\n--- FILE: Security Exception (Blocked) ---\n"

        if not target.exists() or not target.is_file():
            return f"\n--- FILE: {relative_path} (Unreadable) ---\n"

        try:
            content = target.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except OSError:
            return f"\n--- FILE: {relative_path} (Unreadable) ---\n"

        return f"\n--- FILE: {relative_path} ---\n{content}\n----------------------------\n"
