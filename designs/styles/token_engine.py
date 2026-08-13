import json
from pathlib import Path

from pydantic import BaseModel, Field

"""Design Token Engine converting tokens to CSS Variables and Tailwind Config."""


class ColorTokens(BaseModel):
    """Color palette design tokens."""

    primary: str = Field(default="#06b6d4")
    secondary: str = Field(default="#3b82f6")
    accent: str = Field(default="#10b981")
    background: str = Field(default="#0f172a")
    surface: str = Field(default="#1e293b")
    text: str = Field(default="#f8fafc")
    muted: str = Field(default="#94a3b8")
    danger: str = Field(default="#ef4444")


class TokenEngine:
    """Design Tokens Compiler for CSS Variables and Tailwind Config."""

    def __init__(self, token_path: Path | None = None) -> None:
        self.token_path = token_path or Path(__file__).parent / "tokens.json"
        self.colors = ColorTokens()
        self._load_tokens()

    def _load_tokens(self) -> None:
        """Loads token definitions from JSON file."""
        if self.token_path.exists():
            try:
                with self.token_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "colors" in data:
                        self.colors = ColorTokens(**data["colors"])
            except Exception:
                pass

    def generate_css_variables(self) -> str:
        """Generates CSS :root variable definitions."""
        lines = [
            ":root {",
            f"  --color-primary: {self.colors.primary};",
            f"  --color-secondary: {self.colors.secondary};",
            f"  --color-accent: {self.colors.accent};",
            f"  --color-background: {self.colors.background};",
            f"  --color-surface: {self.colors.surface};",
            f"  --color-text: {self.colors.text};",
            f"  --color-muted: {self.colors.muted};",
            f"  --color-danger: {self.colors.danger};",
            "}",
        ]
        return "\n".join(lines)

    def generate_tailwind_colors(self) -> dict[str, str]:
        """Exports color tokens dictionary for Tailwind config."""
        return self.colors.model_dump()
