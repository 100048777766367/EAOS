from fastapi import FastAPI, HTTPException
from packages.identity.application.use_cases import (
    RegisterUserRequest,
    RegisterUserUseCase,
)
from packages.identity.domain.models import User
from packages.identity.infrastructure.adapters import PostgresUserRepository
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
identity_repo = PostgresUserRepository(db_url)


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


@app.post("/users/register", response_model=User, status_code=201)
async def register_user(request: RegisterUserRequest) -> User:
    use_case = RegisterUserUseCase(identity_repo)
    try:
        return use_case.execute(request)
    except ValueError as e:
        # THÊM "from e" VÀO CUỐI DÒNG NÀY:
        raise HTTPException(status_code=400, detail=str(e)) from e