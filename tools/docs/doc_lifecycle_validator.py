"""Documentation lifecycle validator and compliance scanner for EAOS."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class DocumentationAuditDTO(BaseModel):
    """Value object representing a documentation file audit result."""

    model_config = ConfigDict(frozen=True)

    doc_id: str
    file_path: str
    exists: bool
    word_count: int
    has_title: bool


class DocumentLifecycleValidator:
    """Validator auditing technical documentation integrity and presence."""

    MANDATORY_DOCS: tuple[str, ...] = (
        "ARCHITECTURE_CONSTITUTION.md",
        "ENGINEERING_GUIDE.md",
        "PROJECT_CONTEXT.md",
        "CURRENT_CONTEXT.md",
        "ROADMAP.md",
        "TASK.md",
        "ADR_INDEX.md",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.docs_dir: Path = self.root_dir / "docs"

    def audit_core_documentation(self) -> list[DocumentationAuditDTO]:
        """Audits presence and structural readiness of core markdown docs."""
        results: list[DocumentationAuditDTO] = []

        for doc_name in self.MANDATORY_DOCS:
            doc_path = self.docs_dir / doc_name
            exists = doc_path.exists()
            word_count = 0
            has_title = False

            if exists:
                text = doc_path.read_text(encoding="utf-8")
                word_count = len(text.split())
                has_title = "# " in text

            results.append(
                DocumentationAuditDTO(
                    doc_id=doc_name.replace(".md", "").lower(),
                    file_path=str(doc_path.relative_to(self.root_dir) if exists else f"docs/{doc_name}"),
                    exists=exists,
                    word_count=word_count,
                    has_title=has_title,
                )
            )

        return results
