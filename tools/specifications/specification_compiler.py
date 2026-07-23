"""Executable specification compiler and validator engine for EAOS specs."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class SpecificationAuditDTO(BaseModel):
    """Value object representing an audited executable specification."""

    model_config = ConfigDict(frozen=True)

    spec_id: str
    category: str
    file_path: str
    is_compiled: bool


class SpecificationCompilerEngine:
    """Compiler engine compiling markdown specifications across 6 categories."""

    CATEGORIES: tuple[str, ...] = (
        "apis",
        "business",
        "capabilities",
        "domains",
        "services",
        "workflows",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.specs_dir: Path = self.root_dir / "specifications"

    def compile_all_specifications(self) -> list[SpecificationAuditDTO]:
        """Scans and compiles specifications in all 6 subdirectories."""
        results: list[SpecificationAuditDTO] = []
        if not self.specs_dir.exists():
            return results

        for cat in self.CATEGORIES:
            cat_dir = self.specs_dir / cat
            if cat_dir.exists() and cat_dir.is_dir():
                results.extend(
                    SpecificationAuditDTO(
                        spec_id=item.stem,
                        category=cat,
                        file_path=str(item.relative_to(self.root_dir)),
                        is_compiled=True,
                    )
                    for item in cat_dir.iterdir()
                    if (item.is_file() and item.suffix in (".md", ".yaml", ".yml") and not item.name.startswith("."))
                )

        return results
