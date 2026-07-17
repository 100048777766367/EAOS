from packages.knowledge.domain.models import KnowledgeArtifact
from packages.knowledge.domain.ports import KnowledgeRepository
from pydantic import BaseModel


class StoreKnowledgeRequest(BaseModel):
    title: str
    content: str
    author: str


class StoreKnowledgeUseCase:
    """Application Service chịu trách nhiệm lưu trữ tri thức mới."""

    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    def execute(self, request: StoreKnowledgeRequest) -> KnowledgeArtifact:
        # Áp dụng quy tắc nghiệp vụ (ví dụ: lọc/chuẩn hóa dữ liệu đầu vào)
        artifact = KnowledgeArtifact(
            title=request.title.strip(),
            content=request.content.strip(),
            author=request.author.strip(),
        )
        return self.repository.save(artifact)