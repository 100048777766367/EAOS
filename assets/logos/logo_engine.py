from __future__ import annotations

"""Động cơ tiêm theme Dark/Light Mode cho SVG Logos."""


class LogoEngine:
    """Tiêm theme cho Logo SVG."""

    def apply_theme(self, svg_content: str, theme: str) -> str:
        """Thêm thuộc tính theme vào SVG."""
        return f"<!-- Theme: {theme} -->\n{svg_content}"
