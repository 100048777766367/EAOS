"""Knowledge indexing engine for architectural artifacts and Splay cache."""

import time

from pydantic import BaseModel, ConfigDict


class IndexEntryDTO(BaseModel):
    """Value object representing an indexed document entry."""

    model_config = ConfigDict(frozen=True)

    doc_id: str
    title: str
    tags: list[str]


class IndexStatusReport(BaseModel):
    """Value object reporting knowledge index status."""

    model_config = ConfigDict(frozen=True)

    total_indexed: int
    index_version: str


class KnowledgeIndexerEngine:
    """Engine indexing architectural knowledge artifacts."""

    def __init__(self) -> None:
        self._index: dict[str, IndexEntryDTO] = {}

    def index_document(
        self,
        doc_id: str,
        title: str,
        tags: list[str],
    ) -> IndexStatusReport:
        """Indexes a document and updates search registry."""
        entry = IndexEntryDTO(
            doc_id=doc_id,
            title=title,
            tags=tags,
        )
        self._index[doc_id] = entry
        return IndexStatusReport(
            total_indexed=len(self._index),
            index_version=f"v_{int(time.time())}",
        )
