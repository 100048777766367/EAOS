from __future__ import annotations

"""Động cơ xuất chiếu View sơ đồ kiến trúc."""


class ViewEngine:
    """Render sơ đồ C4."""

    def generate_mermaid_c4(self, container_name: str) -> str:
        """Sinh mã Mermaid C4 diagram."""
        return f"C4Container\n  Container({container_name}, 'Service')"
