"""Static structural schema validator engine for EAOS JSON schemas."""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict


class SchemaValidationReportDTO(BaseModel):
    """Value object representing a schema validation audit report."""

    model_config = ConfigDict(frozen=True)

    schema_id: str
    category: str
    file_path: str
    is_valid_json: bool


class SchemaValidatorEngine:
    """Engine verifying static JSON schemas across 6 schema categories."""

    CATEGORIES: tuple[str, ...] = (
        "api",
        "compiler",
        "events",
        "knowledge",
        "representation",
        "storage",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.schemas_dir: Path = self.root_dir / "schemas"

    def validate_all_schemas(self) -> list[SchemaValidationReportDTO]:
        """Scans and validates syntax across all 6 schema subdirectories."""
        results: list[SchemaValidationReportDTO] = []
        if not self.schemas_dir.exists():
            return results

        for cat in self.CATEGORIES:
            cat_dir = self.schemas_dir / cat
            if cat_dir.exists() and cat_dir.is_dir():
                for item in cat_dir.iterdir():
                    if item.is_file() and item.suffix == ".json" and not item.name.startswith("."):
                        is_valid = self._verify_json_syntax(item)
                        results.append(
                            SchemaValidationReportDTO(
                                schema_id=item.stem,
                                category=cat,
                                file_path=str(item.relative_to(self.root_dir)),
                                is_valid_json=is_valid,
                            )
                        )

        return results

    def _verify_json_syntax(self, path: Path) -> bool:
        """Verifies that target file is valid, parseable JSON."""
        try:
            json.loads(path.read_text(encoding="utf-8"))
            return True
        except Exception:
            return False
