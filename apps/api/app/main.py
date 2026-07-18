import os
from typing import Annotated, Any

from fastapi import Body, FastAPI, HTTPException
from kernel.governance.assembly import (
    ArchitectureAssembly,
)
from packages.evolution.domain.models import (
    Evidence,
    check_backwards_compatibility,
    migrate_payload,
)
from packages.evolution.infrastructure.adapters import (
    PostgresEvolutionRepository,
)
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
from packages.knowledge.domain.models import AuditLogEntry, KnowledgeArtifact
from packages.knowledge.infrastructure.adapters import (
    PostgresKnowledgeRepository,
    SplayCacheKnowledgeRepository,
)
from pydantic import BaseModel

app = FastAPI(title="EAOS API Gateway", version="0.1.0")

# Khởi tạo adapter kết nối Postgres qua cổng Docker 5432
db_url = os.getenv(
    "DATABASE_URL",
    "postgresql://eaos:eaos@localhost:5432/eaos",
)

postgres_knowledge_repo = PostgresKnowledgeRepository(db_url)
knowledge_repo = SplayCacheKnowledgeRepository(postgres_knowledge_repo)

identity_repo = PostgresUserRepository(db_url)
evolution_repo = PostgresEvolutionRepository(db_url)


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
async def create_knowledge(
    request: StoreKnowledgeRequest,
) -> KnowledgeArtifact:
    use_case = StoreKnowledgeUseCase(knowledge_repo)
    return use_case.execute(request)


@app.post("/users/register", response_model=User, status_code=201)
async def register_user(request: RegisterUserRequest) -> User:
    use_case = RegisterUserUseCase(identity_repo)
    try:
        return use_case.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


# --- ENDPOINTS TRỰC QUAN HÓA SPLAY TREE GOVERNANCE ---


@app.get("/governance/splay-tree")
async def get_splay_tree_layout() -> dict[str, Any]:
    """Lấy sơ đồ cấu trúc JSON của cây tự tối ưu hóa."""
    return {"root": knowledge_repo.get_tree_layout()}


@app.get("/governance/splay-tree/mermaid")
async def get_splay_tree_mermaid() -> dict[str, str]:
    """Xuất mã đồ thị Mermaid của cây Splay."""
    return {"mermaid": knowledge_repo.get_tree_mermaid()}


@app.get(
    "/governance/audit-logs/{artifact_id}",
    response_model=list[AuditLogEntry],
)
async def get_artifact_audit_logs(artifact_id: str) -> list[AuditLogEntry]:
    """Lấy toàn bộ lịch sử chỉnh sửa (ADD, EDIT, DELETE) của tài liệu."""
    return knowledge_repo.get_audit_logs(artifact_id)


@app.delete("/governance/documents/{artifact_id}")
async def delete_governance_document(
    artifact_id: str,
    author: Annotated[str, Body(embed=True)],
) -> dict[str, str]:
    """Xóa tài liệu khỏi Splay cache và ghi nhận log DELETE."""
    success = knowledge_repo.delete(artifact_id, author)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài liệu trong cache",
        )
    return {
        "message": (
            f"Đã xóa tài liệu {artifact_id} khỏi Splay cache thành công."
        )
    }


# Khởi tạo Hội đồng kiến trúc tự trị
assembly_engine = ArchitectureAssembly()


@app.post(
    "/governance/assembly/commit",
    response_model=dict[str, Any],
    status_code=201,
)
async def commit_to_assembly(
    artifact_id: Annotated[str, Body(embed=True)],
    action: Annotated[str, Body(embed=True)],
    author: Annotated[str, Body(embed=True)],
) -> dict[str, Any]:
    return {}


@app.get("/governance/assembly/ledger", response_model=list[dict[str, Any]])
async def get_assembly_ledger() -> list[dict[str, Any]]:
    return assembly_engine.list_transactions()


# --- ENDPOINTS TIẾN HÓA KIẾN TRÚC (EVOLUTION SPRINT 2) ---


@app.post("/evolution/propose", status_code=201)
async def propose_evolution(
    obj_id: Annotated[str, Body(embed=True)],
    name: Annotated[str, Body(embed=True)],
    payload: Annotated[dict[str, Any], Body(embed=True)],
    author: Annotated[str, Body(embed=True)],
    triggered_by: Annotated[str, Body(embed=True)],
    parent_id: Annotated[str | None, Body(embed=True)] = None,
) -> dict[str, Any]:
    """Đề xuất một phiên bản tiến hóa cấu trúc mới."""
    new_payload = payload.copy()
    version = 1
    if parent_id:
        parent_obj = evolution_repo.find_by_id(parent_id)
        if parent_obj:
            parent_version = parent_obj.payload.get("__version", 1)
            version = parent_version + 1
    new_payload["__version"] = version

    from packages.evolution.domain.models import (
        EvolutionObject,
        Metadata,
        Provenance,
    )

    meta = Metadata(environment="production", criticality="high")
    prov = Provenance(
        author=author,
        triggered_by=triggered_by,
        parent_id=parent_id,
    )
    obj = EvolutionObject(
        id=obj_id,
        name=name,
        payload=new_payload,
        metadata=meta,
        provenance=prov,
        evidences=[],
    )

    saved = evolution_repo.save(obj)
    return {
        "message": "Đề xuất tiến hóa thành công.",
        "id": saved.id,
        "version": version,
        "payload": saved.payload,
    }


@app.post("/evolution/migrate/{doc_id}", status_code=200)
async def migrate_evolution_document(
    doc_id: str,
    rules: Annotated[dict[str, Any], Body(embed=True)],
    author: Annotated[str, Body(embed=True)],
) -> dict[str, Any]:
    """Di chuyển dữ liệu và kiểm nghiệm tương thích ngược cấp cao."""
    parent_obj = evolution_repo.find_by_id(doc_id)
    if not parent_obj:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài liệu cha để di chuyển.",
        )

    new_payload = migrate_payload(parent_obj.payload, rules)
    parent_version = parent_obj.payload.get("__version", 1)
    new_version = parent_version + 1
    new_payload["__version"] = new_version

    compatible, errors = check_backwards_compatibility(
        parent_obj.payload, new_payload
    )
    if not compatible:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Không thể di chuyển do vi phạm tương thích ngược.",
                "errors": errors,
            },
        )

    import uuid

    new_id = f"EVO-{uuid.uuid4().hex[:6].upper()}"

    from packages.evolution.domain.models import (
        EvolutionObject,
        Metadata,
        Provenance,
    )

    meta = Metadata(environment="production", criticality="high")
    prov = Provenance(
        author=author,
        triggered_by="Automatic Schema Migration",
        parent_id=doc_id,
    )

    evidence = Evidence(
        metric_name="Backwards Compatibility check",
        metric_value=1.0,
        passed=True,
        log_summary="Compatibility check passed successfully.",
    )

    obj = EvolutionObject(
        id=new_id,
        name=f"Migrated version of {parent_obj.name}",
        payload=new_payload,
        metadata=meta,
        provenance=prov,
        evidences=[evidence],
    )

    saved = evolution_repo.save(obj)
    return {
        "message": "Di chuyển và kiểm định thành công.",
        "old_id": doc_id,
        "new_id": saved.id,
        "version": new_version,
        "payload": saved.payload,
    }


@app.get("/evolution/lineage/{doc_id}", response_model=list[str])
async def get_document_lineage(doc_id: str) -> list[str]:
    """Truy vết chuỗi gia phả đi ngược về gốc."""
    return evolution_repo.get_lineage(doc_id)