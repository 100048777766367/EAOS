from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Observation:
    name: str
    timestamp: datetime
    value: float
    unit: str = ""


__all__ = ["Observation"]
