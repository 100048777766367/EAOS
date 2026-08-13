from __future__ import annotations

from pathlib import Path

"""Prompt Template Manager."""


class PromptManager:
    """Manager loading and rendering Jinja prompt templates."""

    def __init__(self, prompts_dir: Path | None = None) -> None:
        self.dir = (prompts_dir or Path("AI/prompts")).resolve()

    def load_template(self, template_name: str) -> str:
        """Load prompt template text."""
        path = self.dir / template_name
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""
