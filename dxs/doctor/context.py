from __future__ import annotations

from pathlib import Path


def discover_repository(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() or (candidate / "pyproject.toml").exists():
            return candidate
    return current
