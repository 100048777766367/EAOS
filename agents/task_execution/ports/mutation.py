"""Mutation boundary.

The task execution subsystem does not mutate the repository by itself.
Future mutation adapters must implement this port and remain behind
governance and safety gates.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class MutationPort(Protocol):
    """Controlled repository mutation boundary."""

    async def apply(
        self,
        project_root: Path,
        patch: str,
    ) -> str:
        """Apply an approved patch and return a mutation identifier."""
        ...
