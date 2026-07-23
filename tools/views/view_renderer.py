"""View renderer engine and visual representation manager for EAOS."""

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict


class ViewDefinitionDTO(BaseModel):
    """Value object representing a visual view configuration definition."""

    model_config = ConfigDict(frozen=True)

    view_id: str
    category: str
    title: str
    file_path: str


class ViewRendererEngine:
    """Renderer engine discovering and parsing views across 5 categories."""

    CATEGORIES: tuple[str, ...] = (
        "eaos",
        "foundation",
        "library",
        "research",
        "runtime",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.views_dir: Path = self.root_dir / "views"

    def discover_views(self) -> list[ViewDefinitionDTO]:
        """Scans all 5 view subdirectories for JSON view definition files."""
        results: list[ViewDefinitionDTO] = []
        if not self.views_dir.exists():
            return results

        for cat in self.CATEGORIES:
            cat_dir = self.views_dir / cat
            if cat_dir.exists() and cat_dir.is_dir():
                results.extend(
                    ViewDefinitionDTO(
                        view_id=item.stem,
                        category=cat,
                        title=(f"{cat.capitalize()} {item.stem.replace('_', ' ').title()}"),
                        file_path=str(item.relative_to(self.root_dir)),
                    )
                    for item in cat_dir.iterdir()
                    if (item.is_file() and item.suffix == ".json" and not item.name.startswith("."))
                )

        return results

    def load_view_json(
        self,
        category: str,
        view_file: str,
    ) -> dict[str, Any]:
        """Loads JSON view configuration definition from target path."""
        target_path = self.views_dir / category / view_file
        if target_path.exists():
            try:
                data = json.loads(target_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
            except Exception:
                pass
        return {"status": "NOT_FOUND", "view": view_file}
