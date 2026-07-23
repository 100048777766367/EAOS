"""Bounded context registry mapping enterprise domain contexts."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class BoundedContextDTO(BaseModel):
    """Value object representing a registered bounded context."""

    model_config = ConfigDict(frozen=True)

    context_name: str
    file_path: str
    status: str


class BoundedContextRegistry:
    """Registry discovering and indexing enterprise bounded contexts."""

    CONTEXTS: tuple[str, ...] = (
        "sales",
        "crm",
        "erp",
        "finance",
        "marketing",
        "hr",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.contexts_dir: Path = self.root_dir / "contexts"

    def discover_contexts(self) -> list[BoundedContextDTO]:
        """Scans contexts directory for registered bounded contexts."""
        results: list[BoundedContextDTO] = []
        if not self.contexts_dir.exists():
            return results

        for name in self.CONTEXTS:
            path = self.contexts_dir / name
            exists = path.exists() and path.is_dir()
            results.append(
                BoundedContextDTO(
                    context_name=name,
                    file_path=str(path.relative_to(self.root_dir) if exists else f"contexts/{name}"),
                    status="REGISTERED" if exists else "PLANNED",
                )
            )

        return results
