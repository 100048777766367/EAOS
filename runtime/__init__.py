"""Public entry point for EAOS Runtime Engine."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from runtime.runtime_manager import RuntimeManager


__all__ = ["RuntimeManager"]


def __getattr__(name: str) -> object:
    """Load the runtime facade only when callers request it explicitly."""
    if name == "RuntimeManager":
        from runtime.runtime_manager import RuntimeManager

        return RuntimeManager

    raise AttributeError(name)
