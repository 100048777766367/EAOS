"""Knowledge store engine scanning and indexing organizational memory."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class KnowledgeArtifactDTO(BaseModel):
    """Value object representing an indexed knowledge artifact."""

    model_config = ConfigDict(frozen=True)

    artifact_id: str
    category: str
    file_path: str
    content_summary: str


class KnowledgeStoreEngine:
    """Engine scanning and indexing enterprise knowledge artifacts."""

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

    def scan_knowledge_base(self) -> list[KnowledgeArtifactDTO]:
        """Scans all knowledge subdirectories and returns indexed artifacts."""
        results: list[KnowledgeArtifactDTO] = []
        if not self.knowledge_dir.exists():
            return results

        for cat in self.CATEGORIES:
            cat_path = self.knowledge_dir / cat
            if cat_path.exists() and cat_path.is_dir():
                for item in cat_path.iterdir():
                    if item.is_file() and not item.name.startswith("."):
                        summary = self._safe_read_summary(item)
                        results.append(
                            KnowledgeArtifactDTO(
                                artifact_id=item.stem,
                                category=cat,
                                file_path=str(item.relative_to(self.root_dir)),
                                content_summary=summary,
                            )
                        )

        return results

    def _safe_read_summary(self, item: Path) -> str:
        """Safely reads file content with multi-encoding fallback."""
        try:
            text = item.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                text = item.read_text(encoding="utf-16")
            except Exception:
                text = item.read_text(encoding="utf-8", errors="replace")

        lines = text.splitlines()
        first_line = lines[0] if lines else ""
        return first_line[:100]
