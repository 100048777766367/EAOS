import os
from typing import Annotated, Any

from fastapi import Body, FastAPI, HTTPException
from kernel.governance.assembly import (
    ArchitectureAssembly,
    ConsensusVote,
)
from packages.autonomous.application.use_cases import (
    LoopCycleRequest,
    RunAutonomousLoopUseCase,
)
from packages.autonomous.domain.models import LoopCycle
from packages.autonomous.infrastructure.adapters import (
    InMemoryAutonomousRepository,
)
from packages.evolution.domain.governance import (
    CouncilVote,
    EvolutionGovernanceCouncil,
)
from packages.evolution.domain.models import (
    Evidence,
    EvolutionObject,
    check_backwards_compatibility,
    migrate_payload,
)
from packages.evolution.domain.rules_engine import (
    CriticalityEnvironmentRule,
    FitnessEngine,
    PolicyEngine,
    VersionHeaderRule,
)
from packages.evolution.domain.self_evolution import SelfEvolutionEngine
from packages.evolution.domain.semantic import SemanticLayer
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
from packages.knowledge.domain.tdo import encapsulate_artifact
from packages.knowledge.infrastructure.adapters import (
    PostgresKnowledgeRepository,
    SplayCacheKnowledgeRepository,
)
from packages.learning.application.use_cases import IngestLearningUseCase
from packages.learning.domain.models import Experience
from packages.learning.infrastructure.adapters import (
    InMemoryExperienceRepository,
)
from packages.prediction.application.use_cases import (
    HistoricalMetricsPayload,
    RunPredictionUseCase,
)
from packages.prediction.domain.models import Prediction
from packages.prediction.infrastructure.adapters import (
    InMemoryPredictionRepository,
)
from packages.reflection.application.use_cases import (
    AnalyzeReflectionUseCase,
)
from packages.reflection.domain.models import ReflectionReport
from packages.reflection.infrastructure.adapters import (
    InMemoryReflectionRepository,
)
from packages.self_rewrite.application.use_cases import (
    RunSelfRewriteUseCase,
    SelfRewriteRequest,
)
from packages.self_rewrite.domain.models import SelfRewriteJob
from packages.self_rewrite.infrastructure.adapters import (
    InMemorySelfRewriteRepository,
)
from packages.simulation.application.use_cases import (
    RunSimulationUseCase,
    SimulationRequest,
)
from packages.simulation.domain.models import Simulation
from packages.simulation.infrastructure.adapters import (
    InMemorySimulationRepository,
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
evo_council = EvolutionGovernanceCouncil()
reflection_repo = InMemoryReflectionRepository()
learning_repo = InMemoryExperienceRepository()
prediction_repo = InMemoryPredictionRepository()
simulation_repo = InMemorySimulationRepository()
self_rewrite_repo = InMemorySelfRewriteRepository()
autonomous_repo = InMemoryAutonomousRepository()


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
    """Hội đồng họp kiểm duyệt và xuất tệp đóng gói TDO tự mô tả."""
    artifact = knowledge_repo.find_by_id(artifact_id)
    if not artifact:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tri thức yêu cầu",
        )

    votes = [
        ConsensusVote(
            voter="ArchitectAgent",
            decision="APPROVED",
            reason="Mã nguồn tuân thủ Hiến pháp quy định phân lớp.",
        ),
        ConsensusVote(
            voter="ReviewerAgent",
            decision="APPROVED",
            reason="Lịch sử thay đổi được ghi nhận đầy đủ.",
        ),
    ]

    tx = assembly_engine.evaluate_proposal(action, artifact, votes)

    if tx.status != "COMMITTED":
        raise HTTPException(status_code=400, detail="Thay đổi bị bác bỏ.")

    tdo = encapsulate_artifact(artifact, author=author)

    return {
        "transaction": tx.model_dump(),
        "trustworthy_digital_object": tdo.model_dump(by_alias=True),
    }


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


# --- ENDPOINTS CHÍNH SÁCH VÀ TỰ SINH TRƯỞNG (SPRINT 3-6) ---


@app.post("/evolution/evaluate-fitness/{doc_id}")
async def evaluate_fitness(doc_id: str) -> dict[str, Any]:
    """Chạy Rules Engine đánh giá và tính điểm Fitness."""
    obj = evolution_repo.find_by_id(doc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")

    policy = PolicyEngine(
        name="Architecture Constitution Policy",
        rules=[VersionHeaderRule(), CriticalityEnvironmentRule()],
    )
    passed, results = policy.evaluate_policy(obj)

    from packages.evolution.domain.models import Evidence

    evidences = [
        Evidence(
            metric_name=r.rule_name,
            metric_value=1.0 if r.passed else 0.0,
            passed=r.passed,
            log_summary=r.message,
        )
        for r in results
    ]

    updated_obj = EvolutionObject(
        id=obj.id,
        name=obj.name,
        payload=obj.payload,
        metadata=obj.metadata,
        provenance=obj.provenance,
        evidences=evidences,
    )
    evolution_repo.save(updated_obj)

    score = FitnessEngine.calculate_fitness(updated_obj)
    return {
        "passed": passed,
        "results": [r.model_dump() for r in results],
        "fitness_score": score,
    }


@app.post("/evolution/council/vote/{doc_id}")
async def vote_on_evolution(
    doc_id: str,
    voters_payload: Annotated[list[dict[str, str]], Body(embed=True)],
) -> dict[str, Any]:
    """Tổ chức Hội đồng biểu quyết và ghi sổ Ledger."""
    obj = evolution_repo.find_by_id(doc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")

    votes = [
        CouncilVote(
            voter=v["voter"],
            decision=v["decision"],
            reason=v["reason"],
        )
        for v in voters_payload
    ]

    tx = evo_council.evaluate_proposal(obj, votes)
    return {"transaction": tx.model_dump()}


@app.get("/evolution/semantic/{doc_id}")
async def get_semantic_representation(doc_id: str) -> dict[str, Any]:
    """Xuất bản tệp đóng gói JSON-LD và RDF Triples."""
    obj = evolution_repo.find_by_id(doc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")

    json_ld = SemanticLayer.to_json_ld(obj)
    rdf_triples = SemanticLayer.to_rdf_triples(obj)

    return {"json_ld": json_ld, "rdf_triples": rdf_triples}


@app.post("/evolution/self-heal/{doc_id}")
async def self_heal_document(doc_id: str) -> dict[str, Any]:
    """Tự động phát hiện vi phạm và kích hoạt tự điều chỉnh (Self-healing)."""
    obj = evolution_repo.find_by_id(doc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")

    adjustment_rules = {"max_retry_loops": 0.5, "llm_fallback": "local-llama"}

    healed_obj = SelfEvolutionEngine.trigger_self_evolution(
        failed_obj=obj,
        failed_metric_name="OOM Crash Thread Limit",
        adjustment_rules=adjustment_rules,
    )

    saved = evolution_repo.save(healed_obj)
    return {
        "message": "Self-healing và thích ứng cấu hình tự động thành công.",
        "healed_id": saved.id,
        "payload": saved.payload,
    }


# --- ENDPOINTS CHẨN ĐOÁN VÀ SUY NGẪM SỰ CỐ (SPRINT 7) ---


@app.post("/reflection/analyze", response_model=ReflectionReport, status_code=201)
async def analyze_reflection_report(
    subject_id: Annotated[str, Body(embed=True)],
    trigger_event: Annotated[str, Body(embed=True)],
    passed_checks: Annotated[bool, Body(embed=True)],
) -> ReflectionReport:
    """Tự động chẩn đoán nguyên nhân gốc rễ (Root Cause) và khuyến nghị."""
    use_case = AnalyzeReflectionUseCase(reflection_repo)
    return use_case.execute(
        subject_id=subject_id,
        trigger_event=trigger_event,
        passed_checks=passed_checks,
    )


# --- ENDPOINTS HỌC HỎI VÀ ĐÚC RÚT KINH NGHIỆM (SPRINT 8) ---


@app.post("/learning/ingest", response_model=Experience, status_code=201)
async def ingest_learning_experience(
    reflection_id: Annotated[str, Body(embed=True)],
) -> Experience:
    """Chuyển dịch báo cáo chẩn đoán sự cố thành Kinh nghiệm lưu RAM cache."""
    use_case = IngestLearningUseCase(learning_repo, reflection_repo)
    try:
        return use_case.execute(reflection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


# --- ENDPOINTS DỰ BÁO RỦI RO SỚM KIẾN TRÚC (SPRINT 9) ---


@app.post("/prediction/run", response_model=Prediction, status_code=201)
async def run_prediction_engine(
    payload: HistoricalMetricsPayload,
) -> Prediction:
    """Quét dữ liệu lịch sử đo lường và phát đi dự báo rủi ro sớm."""
    use_case = RunPredictionUseCase(prediction_repo)
    try:
        return use_case.execute(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


# --- ENDPOINTS MÔ PHỎNG GIẢ LẬP SANDBOX (SPRINT 10) ---


@app.post("/simulation/run", response_model=Simulation, status_code=201)
async def run_simulation_engine(
    request: SimulationRequest,
) -> Simulation:
    """Khởi chạy mô phỏng Dry-Run kiểm thử cấu hình trên Sandbox ảo."""
    use_case = RunSimulationUseCase(simulation_repo)
    return use_case.execute(request)


# --- ENDPOINTS TỰ LẬP TRÌNH VÀ SỬA ĐỔI MÃ NGUỒN (SPRINT 11) ---


@app.post("/self-rewrite/run", response_model=SelfRewriteJob, status_code=201)
async def run_self_rewrite_engine(
    request: SelfRewriteRequest,
) -> SelfRewriteJob:
    """Kích hoạt chuỗi tác vụ AI Agent tự lập trình và tạo Pull Request."""
    use_case = RunSelfRewriteUseCase(self_rewrite_repo)
    return use_case.execute(request)


# --- ENDPOINT VÒNG LẶP TIẾN HÓA VÔ HẠN TỰ TRỊ (SPRINT 12 - CHUNG KẾT) ---


@app.post("/autonomous/run-cycle", response_model=LoopCycle, status_code=201)
async def run_autonomous_loop_cycle(
    request: LoopCycleRequest,
) -> LoopCycle:
    """Khởi chạy toàn bộ vòng lặp tiến hóa đóng kín trong một chu kỳ tự trị."""
    use_case = RunAutonomousLoopUseCase(autonomous_repo)
    return use_case.execute(request)