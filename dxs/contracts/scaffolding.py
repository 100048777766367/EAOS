from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ScaffoldResult:
    root: Path
    created: tuple[Path, ...]
    skipped: tuple[Path, ...]
