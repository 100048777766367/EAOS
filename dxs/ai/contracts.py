from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class AIRequest:
    """Request crossing the DXS AI boundary."""

    capability: str
    prompt: str
    metadata: Mapping[str, str] | None = None


@dataclass(frozen=True)
class AIResponse:
    """Response returned through the DXS AI boundary."""

    capability: str
    content: str
    success: bool = True
    metadata: Mapping[str, str] | None = None
