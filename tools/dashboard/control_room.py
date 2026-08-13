from __future__ import annotations

from pathlib import Path

"""Control Room Dashboard Renderer Module."""


class ControlRoomDashboard:
    """Renders enterprise dashboard HTML from decoupled templates."""

    def __init__(self, root_path: Path | None = None) -> None:
        self._root = root_path or Path("D:/EAOS").resolve()
        self._template_file = self._root / "tools" / "dashboard" / "templates" / "dashboard.html"

    def render_html(self) -> str:
        """Load and return rendered HTML content."""
        if not self._template_file.exists():
            return "<html><body><h1>Dashboard Template Missing</h1></body></html>"
        return self._template_file.read_text(encoding="utf-8")
