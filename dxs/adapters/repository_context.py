from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from dxs.domain.repository import (
    RepositoryContext,
    SourceDocument,
)


class RepositoryContextProvider:
    """Resolve EAOS repository sources of truth."""

    SOURCES: ClassVar[dict[str, tuple[str, ...]]] = {
        "architecture_constitution": ("ARCHITECTURE_CONSTITUTION.md",),
        "engineering_guide": ("ENGINEERING_GUIDE.md",),
        "project_context": (
            "docs/PROJECT_CONTEXT.md",
            "PROJECT_CONTEXT.md",
        ),
        "current_context": (
            "docs/CURRENT_CONTEXT.md",
            "CURRENT_CONTEXT.md",
        ),
        "task": (
            "docs/TASK.md",
            "TASK.md",
        ),
        "adr_index": (
            "docs/ADR_INDEX.md",
            "ADR_INDEX.md",
        ),
        "roadmap": (
            "docs/ROADMAP.md",
            "ROADMAP.md",
        ),
        "governance": (
            "GOVERNANCE.md",
            "docs/GOVERNANCE.md",
        ),
        "repository_contract": (".eaos/contracts/repository-contract.yaml",),
        "repository_specification": ("specifications/repository-spec.md",),
    }

    ROLES: ClassVar[dict[str, str]] = {
        "architecture_constitution": "supreme_source_of_truth",
        "engineering_guide": "engineering_standard",
        "project_context": "project_context",
        "current_context": "current_state",
        "task": "execution_plan",
        "adr_index": "architecture_decisions",
        "roadmap": "strategic_direction",
        "governance": "repository_governance",
        "repository_contract": "repository_contract",
        "repository_specification": "repository_specification",
    }

    def discover(self, root: Path) -> RepositoryContext:
        root = root.resolve()

        return RepositoryContext(
            root=root,
            architecture_constitution=self._resolve(
                root,
                "architecture_constitution",
            ),
            engineering_guide=self._resolve(
                root,
                "engineering_guide",
            ),
            project_context=self._resolve(
                root,
                "project_context",
            ),
            current_context=self._resolve(
                root,
                "current_context",
            ),
            task=self._resolve(
                root,
                "task",
            ),
            adr_index=self._resolve(
                root,
                "adr_index",
            ),
            roadmap=self._resolve(
                root,
                "roadmap",
            ),
            governance=self._resolve(
                root,
                "governance",
            ),
            repository_contract=self._resolve(
                root,
                "repository_contract",
            ),
            repository_specification=self._resolve(
                root,
                "repository_specification",
            ),
        )

    def _resolve(
        self,
        root: Path,
        key: str,
    ) -> SourceDocument:
        candidates = self.SOURCES[key]

        for relative_path in candidates:
            path = root / relative_path

            if path.is_file():
                return SourceDocument(
                    key=key,
                    path=path,
                    role=self.ROLES[key],
                )

        # Preserve the canonical first candidate as the
        # expected location when the source is missing.
        return SourceDocument(
            key=key,
            path=root / candidates[0],
            role=self.ROLES[key],
        )
