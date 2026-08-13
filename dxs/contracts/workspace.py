from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class WorkspaceContext:
    root: Path

    def resolve(self, relative: str | Path) -> Path:
        return self.root / relative
