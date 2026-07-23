"""Static assets registry and template loader for EAOS."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class AssetMetadataDTO(BaseModel):
    """Value object representing static asset metadata."""

    model_config = ConfigDict(frozen=True)

    asset_id: str
    category: str
    file_path: str
    file_size_bytes: int


class AssetManager:
    """Manager loading and validating architectural assets and templates."""

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.assets_dir: Path = self.root_dir / "assets"

    def discover_assets(
        self,
        category: str = "templates",
    ) -> list[AssetMetadataDTO]:
        """Scans target assets directory and builds metadata list."""
        target_path = self.assets_dir / category
        if not target_path.exists():
            return []

        file_items = [f for f in target_path.iterdir() if f.is_file() and not f.name.startswith(".")]

        return [
            AssetMetadataDTO(
                asset_id=item.stem,
                category=category,
                file_path=str(item.relative_to(self.root_dir)),
                file_size_bytes=item.stat().st_size,
            )
            for item in file_items
        ]

    def load_template_text(
        self,
        template_name: str = "architecture_document_template.md",
    ) -> str:
        """Loads template markdown content from assets/templates/."""
        template_path = self.assets_dir / "templates" / template_name
        if template_path.exists():
            return template_path.read_text(encoding="utf-8")
        return f"# Template {template_name} Not Found"
