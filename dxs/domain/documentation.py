from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DocumentationResult:
    name: str
    passed: bool
    message: str

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.name}: {self.message}"


class DocumentationService:
    """Inspect authoritative EAOS documentation files."""

    DOCUMENTS = (
        "ARCHITECTURE_CONSTITUTION.md",
        "ENGINEERING_GUIDE.md",
        "GOVERNANCE.md",
        "docs/PROJECT_CONTEXT.md",
        "docs/CURRENT_CONTEXT.md",
        "docs/TASK.md",
        "docs/ADR_INDEX.md",
        "docs/ROADMAP.md",
    )

    def inspect(self, root: Path) -> list[DocumentationResult]:
        return [self._inspect(root, item) for item in self.DOCUMENTS]

    @staticmethod
    def _inspect(root: Path, relative: str) -> DocumentationResult:
        path = root / relative
        passed = path.exists() and path.is_file()

        return DocumentationResult(
            name=relative,
            passed=passed,
            message=str(path),
        )
