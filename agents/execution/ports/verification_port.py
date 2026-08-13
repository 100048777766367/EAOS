"""Verification port."""

from __future__ import annotations

from typing import Any, Protocol


class VerificationPort(Protocol):
    """Port to the existing EAOS verification subsystem."""

    async def verify(self) -> dict[str, Any]:
        """Run verification."""
        ...
