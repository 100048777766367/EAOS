from fastapi import FastAPI
from packages.knowledge.application.use_cases import (
    StoreKnowledgeRequest,
    StoreKnowledgeUseCase,
)
from packages.knowledge.domain.models import KnowledgeArtifact
from packages.knowledge.infrastructure.adapters import (
    PostgresKnowledgeRepository,
)
from pydantic import BaseModel

app = FastAPI(title="EAOS API Gateway", version="0.1.0")

# Khởi tạo adapter kết nối Postgres qua cổng Docker 5432
db_url = "postgresql://eaos:eaos@localhost:5432/eaos"
knowledge_repo = PostgresKnowledgeRepository(db_url)


class HealthResponse(BaseModel):
    status: str
    version: str
    governance: str


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        governance="ARCHITECTURE_CONSTITUTION.md v2.0",
    )


@app.post("/knowledge", response_model=KnowledgeArtifact, status_code=201)
async def create_knowledge(request: StoreKnowledgeRequest) -> KnowledgeArtifact:
    use_case = StoreKnowledgeUseCase(knowledge_repo)
    return use_case.execute(request)