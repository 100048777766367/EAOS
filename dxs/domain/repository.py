from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SourceDocument:
    key: str
    path: Path
    role: str

    @property
    def exists(self) -> bool:
        return self.path.is_file()


@dataclass(frozen=True, slots=True)
class RepositoryContext:
    root: Path
    architecture_constitution: SourceDocument
    engineering_guide: SourceDocument
    project_context: SourceDocument
    current_context: SourceDocument
    task: SourceDocument
    adr_index: SourceDocument
    roadmap: SourceDocument
    governance: SourceDocument
    repository_contract: SourceDocument
    repository_specification: SourceDocument

    @property
    def documents(self) -> tuple[SourceDocument, ...]:
        return (
            self.architecture_constitution,
            self.engineering_guide,
            self.project_context,
            self.current_context,
            self.task,
            self.adr_index,
            self.roadmap,
            self.governance,
            self.repository_contract,
            self.repository_specification,
        )

    @property
    def missing(self) -> tuple[SourceDocument, ...]:
        return tuple(document for document in self.documents if not document.exists)
