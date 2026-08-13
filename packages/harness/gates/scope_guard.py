from __future__ import annotations

from pathlib import Path


class ScopeViolationError(Exception):
    """Raised when target path escapes workspace root."""


class ScopeGuard:
    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root: Path = (workspace_root or Path.cwd()).resolve()

    def validate_target_path(self, target_uri: str | Path | None) -> Path:
        if target_uri is None:
            return self.root
        target = Path(target_uri)
        resolved = (self.root / target).resolve() if not target.is_absolute() else target.resolve()

        try:
            resolved.relative_to(self.root)
        except ValueError as err:
            raise ScopeViolationError(
                f"Scope Violation: Path '{resolved}' escapes workspace root '{self.root}'."
            ) from err
        return resolved
