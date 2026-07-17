from typing import Protocol

from packages.knowledge.domain.models import KnowledgeArtifact


class KnowledgeRepository(Protocol):
    """Port (Interface) định nghĩa các hành vi lưu trữ tri thức."""

    def save(self, artifact: KnowledgeArtifact) -> KnowledgeArtifact: ...

    def find_by_id(self, artifact_id: str) -> KnowledgeArtifact | None: ...