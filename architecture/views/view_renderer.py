from __future__ import annotations

from architecture.models.c4_model import C4Element

"""Architecture View Renderer and Diagram Generator."""


class ViewRenderer:
    """Renderer producing architectural view representations."""

    def render_c4_summary(self, elements: list[C4Element]) -> str:
        """Render text summary of C4 elements."""
        lines = ["=== C4 Architecture View Summary ==="]
        lines.extend(f"[{elem.layer_type}] {elem.name} ({elem.technology})" for elem in elements)
        return "\n".join(lines)
