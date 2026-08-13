from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Policy:
    name: str
    enabled: bool = True
    description: str = ""


__all__ = ["Policy"]