from __future__ import annotations

from collections.abc import Sequence

from architecture.models.c4_model import C4Element

"""Mermaid diagram exporter."""


class MermaidExporter:
    """Mermaid diagram exporter."""

    def export_c4_diagram(self, elements: Sequence[C4Element]) -> str:
        """Export C4 elements to Mermaid string."""
        names = ", ".join(e.name for e in elements)
        return "graph TD\n  subgraph EAOS\n    " + names + "\n  end"
