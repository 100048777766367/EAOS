"""Knowledge repository scanner and organizational memory auditor for EAOS."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class KnowledgeCategoryDTO(BaseModel):
    """Value object representing an indexed knowledge category."""

    model_config = ConfigDict(frozen=True)

    category: str
    item_count: int
    file_paths: list[str]


class KnowledgeRepositoryScanner:
    """Scanner indexing and auditing declarative knowledge artifacts."""

    CATEGORIES: tuple[str, ...] = (
        "adr",
        "artifacts",
        "axioms",
        "concepts",
        "constitutions",
        "decisions",
        "discussions",
        "evidence",
        "experiments",
        "glossary",
        "hypotheses",
        "metamodels",
        "ontologies",
        "patterns",
        "primitives",
        "principles",
        "templates",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.knowledge_dir: Path = self.root_dir / "knowledge"

    def scan_knowledge_base(self) -> list[KnowledgeCategoryDTO]:
        """Scans all 17 knowledge base subdirectories and indexes artifacts."""
        results: list[KnowledgeCategoryDTO] = []
        if not self.knowledge_dir.exists():
            return results

        for cat in self.CATEGORIES:
            cat_path = self.knowledge_dir / cat
            file_paths: list[str] = []

            if cat_path.exists() and cat_path.is_dir():
                file_items = [item for item in cat_path.iterdir() if item.is_file() and not item.name.startswith(".")]
                file_paths.extend(str(item.relative_to(self.root_dir)) for item in file_items)

            results.append(
                KnowledgeCategoryDTO(
                    category=cat,
                    item_count=len(file_paths),
                    file_paths=file_paths,
                )
            )

        return results
