from pydantic import BaseModel

from packages.knowledge.domain.models import KnowledgeArtifact
from packages.knowledge.domain.ports import KnowledgeRepository


class StoreKnowledgeRequest(BaseModel):
    title: str
    content: str
    author: str


class StoreKnowledgeUseCase:
    """Application Service chá»‹u trÃ¡ch nhiá»‡m lÆ°u trá»¯ tri thá»©c má»›i."""

    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    def execute(self, request: StoreKnowledgeRequest) -> KnowledgeArtifact:
        # Ãp dá»¥ng quy táº¯c nghiá»‡p vá»¥ (vÃ­ dá»¥: lá»c/chuáº©n hÃ³a dá»¯ liá»‡u Ä‘áº§u vÃ o)
        artifact = KnowledgeArtifact(
            title=request.title.strip(),
            content=request.content.strip(),
            author=request.author.strip(),
        )
        return self.repository.save(artifact)
