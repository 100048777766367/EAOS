from __future__ import annotations

from pathlib import Path
from typing import Any

"""Architecture template engine."""


class ArchitectureTemplateEngine:
    """Architecture template engine implementation."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.workspace_root = workspace_root or Path(".")

    def render_template(self, template_name: str, context: dict[str, Any]) -> str:
        """Render template with context variables."""
        title = str(context.get("TITLE", "Document"))
        return "# " + title + "\n\nRendered document template: " + str(template_name)
