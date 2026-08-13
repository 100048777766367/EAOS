from __future__ import annotations

"""Động cơ xử lý biểu tượng SVG Icons."""


class IconEngine:
    """Tối ưu hóa tệp SVG Icon."""

    def verify_svg_icon(self, svg_content: str) -> bool:
        """Kiểm tra tệp SVG hợp lệ."""
        return "<svg" in svg_content and "</svg>" in svg_content
