from typing import Protocol

from packages.knowledge.domain.models import KnowledgeArtifact


class KnowledgeRepository(Protocol):
    """Port (Interface) Ä‘á»‹nh nghÄ©a cÃ¡c hÃ nh vi lÆ°u trá»¯ tri thá»©c."""

    def save(self, artifact: KnowledgeArtifact) -> KnowledgeArtifact: ...

    def find_by_id(self, artifact_id: str) -> KnowledgeArtifact | None: ...
