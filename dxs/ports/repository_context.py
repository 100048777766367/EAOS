from __future__ import annotations

from pathlib import Path
from typing import Protocol

from dxs.domain.repository import RepositoryContext


class RepositoryContextProvider(Protocol):
    def discover(self, root: Path) -> RepositoryContext: ...
