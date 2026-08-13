"""Ports for the EAOS verification subsystem."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Protocol

from .models import VerificationRun

VerificationEvent = Callable[
    [dict[str, object]],
    Awaitable[None],
]


class VerificationRunner(Protocol):
    """Protocol implemented by verification runners."""

    name: str

    async def run(
        self,
        project_root: Path,
    ) -> VerificationRun:
        """Execute the verification runner."""
        ...


class EvidenceStore(Protocol):
    """Protocol for verification evidence storage."""

    def store(
        self,
        result: dict[str, object],
    ) -> str:
        """Persist verification evidence."""
        ...
