from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

"""C4 model definitions."""


class C4LayerType(StrEnum):
    """C4 layer types."""

    CONTEXT = "CONTEXT"
    CONTAINER = "CONTAINER"
    COMPONENT = "COMPONENT"
    CODE = "CODE"


@dataclass
class C4Element:
    """C4 Element DTO."""

    element_id: str
    name: str
    layer_type: C4LayerType
    technology: str = ""
