from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

"""Visual asset loader module."""


@dataclass
class VisualAssetDTO:
    """Visual asset DTO."""

    asset_type: str = "SVG"
    svg_content: str = "<svg><rect/></svg>"


class VisualAssetLoader:
    """Visual asset loader implementation."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.workspace_root = workspace_root or Path(".")

    def load_svg_asset(self, category: str, filename: str) -> VisualAssetDTO:
        """Load visual SVG asset."""
        return VisualAssetDTO()
