from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

"""Diagram manager module."""


@dataclass
class DiagramAssetDTO:
    """Diagram asset DTO."""

    diagram_id: str = "system_architecture_overview"
    content: str = "graph TD\n  A[EAOS Platform] --> B[Services]"


class DiagramManager:
    """Diagram manager implementation."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.workspace_root = workspace_root or Path(".")

    def load_diagram(self, filename: str) -> DiagramAssetDTO:
        """Load diagram asset by filename."""
        diag_id = filename.replace(".mermaid", "").replace(".puml", "")
        return DiagramAssetDTO(diagram_id=diag_id)
