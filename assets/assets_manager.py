from __future__ import annotations

from .diagrams.diagram_manager import DiagramManager

"""Assets manager."""


class AssetsManager:
    """Assets manager."""

    def __init__(self) -> None:
        self.diagram_manager = DiagramManager()
