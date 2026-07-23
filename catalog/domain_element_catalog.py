"""Domain element catalog indexing entities, events, commands, and queries."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class DomainElementDTO(BaseModel):
    """Value object representing an indexed domain element."""

    model_config = ConfigDict(frozen=True)

    element_type: str
    item_count: int
    status: str


class DomainElementCatalog:
    """Catalog indexing domain entities, events, commands, and aggregates."""

    ELEMENT_TYPES: tuple[str, ...] = (
        "entities",
        "events",
        "commands",
        "queries",
        "aggregates",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.catalog_dir: Path = self.root_dir / "catalog"

    def audit_domain_catalog(self) -> list[DomainElementDTO]:
        """Audits domain elements across all 5 catalog categories."""
        results: list[DomainElementDTO] = []
        if not self.catalog_dir.exists():
            return results

        for elem_type in self.ELEMENT_TYPES:
            type_dir = self.catalog_dir / elem_type
            exists = type_dir.exists() and type_dir.is_dir()
            count = len([f for f in type_dir.iterdir() if f.is_file()]) if exists else 0

            results.append(
                DomainElementDTO(
                    element_type=elem_type,
                    item_count=count,
                    status="ACTIVE" if exists else "UNINITIALIZED",
                )
            )

        return results
