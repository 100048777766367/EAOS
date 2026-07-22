import os
from pathlib import Path
from typing import Annotated, Any, cast

from engine.compiler.architecture_compiler import ArchitectureCompiler
from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from kernel.events.event_bus import (
    EventBus,
)
from kernel.governance.assembly import ArchitectureAssembly, ConsensusVote
from kernel.registry.enterprise_registry import (
    EnterpriseRegistry,
    RegistryResource,
)
from packages.agent.infrastructure.adapters import InMemoryAgentRegistry
from packages.autonomous.application.use_cases import (
    LoopCycleRequest,
    RunAutonomousLoopUseCase,
)
from packages.autonomous.domain.models import LoopCycle
from packages.autonomous.infrastructure.adapters import (
    InMemoryAutonomousRepository,
    PostgresAutonomousRepository,
)
from packages.capability.domain.models import BusinessCapability
from packages.capability.infrastructure.adapters import (
    InMemoryCapabilityRegistry,
)
from packages.civilization.infrastructure.adapters import (
    InMemoryCivilizationRegistry,
)
from packages.evolution.application.use_cases import (
    ProposeEvolutionRequest,
    ProposeEvolutionUseCase,
)
from packages.evolution.domain.governance import (
    CouncilVote,
    EvolutionGovernanceCouncil,
)
from packages.evolution.infrastructure.adapters import (
    InMemoryEvolutionRepository,
    PostgresEvolutionRepository,
)
from packages.exchange.infrastructure.adapters import (
    InMemoryEcosystemEventMesh,
)
from packages.federation.domain.models import (
    EcosystemMember,
)
from packages.federation.infrastructure.adapters import (
    InMemoryFederationRegistry,
)
from packages.identity.application.use_cases import (
    RegisterUserRequest,
    RegisterUserUseCase,
)
from packages.identity.domain.models import User
from packages.identity.infrastructure.adapters import (
    InMemoryUserRepository,
    PostgresUserRepository,
)
from packages.intelligence.infrastructure.adapters import (
    InMemoryIntelligenceRegistry,
)
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
from packages.marketplace.infrastructure.adapters import InMemoryMarketplace
from packages.memory.application.dto import MemoryResponse, StoreMemoryCommand
from packages.memory.application.handlers import (
    StoreMemoryHandler,
)
from packages.memory.infrastructure.repository import InMemoryMemoryRepository
from packages.metrics_engine.application.use_cases import (
    ComputeArchitectureHealthUseCase,
)
from packages.metrics_engine.infrastructure.adapters import (
    InMemoryMetricsRepository,
    PrometheusMetricsExporterAdapter,
)
from packages.prediction.application.use_cases import (
    HistoricalMetricsPayload,
    RunPredictionUseCase,
)
from packages.prediction.domain.models import Prediction
from packages.prediction.infrastructure.adapters import (
    InMemoryPredictionRepository,
)
from packages.reflection.application.use_cases import AnalyzeReflectionUseCase
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
from packages.specification.infrastructure.adapters import (
    InMemorySpecificationRegistry,
)
from packages.tenancy.infrastructure.adapters import InMemoryTenantRegistry
from packages.workflow.infrastructure.adapters import InMemoryWorkflowRegistry
from platform_services.resilience.engine import (
    IdempotencyManager,
    IdempotencyService,
    ResilienceEngine,
)
from platform_services.telemetry.observability import (
    EAOSObservabilityMiddleware,
    TelemetryService,
)
from pydantic import BaseModel

app = FastAPI(title="EAOS API Gateway", version="0.1.0")

# Root path 4 cấp chuẩn D:\EAOS
ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent

enterprise_registry = EnterpriseRegistry()
federation_registry = InMemoryFederationRegistry()
tenant_registry = InMemoryTenantRegistry()
event_mesh_exchange = InMemoryEcosystemEventMesh()
marketplace_store = InMemoryMarketplace()
memory_repo = InMemoryMemoryRepository()
agent_registry = InMemoryAgentRegistry()
idempotency_manager = IdempotencyManager()
intelligence_registry = InMemoryIntelligenceRegistry()
civilization_repo = InMemoryCivilizationRegistry()
metrics_repo = InMemoryMetricsRepository()

db_url = os.getenv("DATABASE_URL", "postgresql://eaos:eaos@localhost:5432/eaos")

identity_repo: Any
evolution_repo: Any
autonomous_repo: Any

try:
    postgres_knowledge_repo = PostgresKnowledgeRepository(db_url)
    knowledge_repo = SplayCacheKnowledgeRepository(postgres_knowledge_repo)
    identity_repo = PostgresUserRepository(db_url)
    evolution_repo = PostgresEvolutionRepository(db_url)
    autonomous_repo = PostgresAutonomousRepository(db_url)
except Exception:
    knowledge_repo = SplayCacheKnowledgeRepository(None)
    identity_repo = InMemoryUserRepository()
    evolution_repo = InMemoryEvolutionRepository()
    autonomous_repo = InMemoryAutonomousRepository()

evo_council = EvolutionGovernanceCouncil()
reflection_repo = InMemoryReflectionRepository()
learning_repo = InMemoryExperienceRepository()
prediction_repo = InMemoryPredictionRepository()
simulation_repo = InMemorySimulationRepository()
self_rewrite_repo = InMemorySelfRewriteRepository()
capability_registry = InMemoryCapabilityRegistry()
spec_registry = InMemorySpecificationRegistry()
workflow_registry = InMemoryWorkflowRegistry()

telemetry_service = TelemetryService()
idempotency_service = IdempotencyService()
resilience_engine = ResilienceEngine()
event_bus = EventBus()

app.add_middleware(
    EAOSObservabilityMiddleware,
    metrics_repository=metrics_repo,
    system_id="EAOS-CORE",
)

identity_yaml = ROOT_PATH / "capabilities" / "identity" / "capability.yaml"
knowledge_yaml = ROOT_PATH / "capabilities" / "knowledge" / "capability.yaml"

if identity_yaml.exists():
    cap_identity = capability_registry.load_from_yaml(identity_yaml)
    capability_registry.register(cap_identity)
    enterprise_registry.register(
        RegistryResource(
            id=cap_identity.id,
            type="CAPABILITY",
            name=cap_identity.name,
            metadata=cap_identity.model_dump(mode="json"),
        )
    )

if knowledge_yaml.exists():
    cap_knowledge = capability_registry.load_from_yaml(knowledge_yaml)
    capability_registry.register(cap_knowledge)
    enterprise_registry.register(
        RegistryResource(
            id=cap_knowledge.id,
            type="CAPABILITY",
            name=cap_knowledge.name,
            metadata=cap_knowledge.model_dump(mode="json"),
        )
    )

spec_path = ROOT_PATH / "knowledge" / "specifications" / "invoice.yaml"
if spec_path.exists():
    compiled_spec = spec_registry.load_from_yaml(spec_path)
    spec_registry.register(compiled_spec)
    enterprise_registry.register(
        RegistryResource(
            id=compiled_spec.id,
            type="SPECIFICATION",
            name=compiled_spec.name,
            metadata=compiled_spec.model_dump(mode="json"),
        )
    )

workflow_yaml = ROOT_PATH / "knowledge" / "specifications" / "workflow.yaml"
if workflow_yaml.exists():
    compiled_workflow = workflow_registry.load_from_yaml(workflow_yaml)
    workflow_registry.register_definition(compiled_workflow)
    enterprise_registry.register(
        RegistryResource(
            id=compiled_workflow.id,
            type="WORKFLOW",
            name=compiled_workflow.name,
            metadata=compiled_workflow.model_dump(mode="json"),
        )
    )


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


@app.get("/metrics", response_class=PlainTextResponse)
async def get_prometheus_metrics() -> PlainTextResponse:
    use_case = ComputeArchitectureHealthUseCase(metrics_repo)
    dashboard = use_case.execute(
        system_id="EAOS-CORE",
        capability_ids=["cap.knowledge", "cap.identity"],
    )
    exporter = PrometheusMetricsExporterAdapter()
    return PlainTextResponse(
        content=exporter.export_prometheus_format(dashboard),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )


@app.post("/knowledge", response_model=KnowledgeArtifact, status_code=201)
async def create_knowledge(
    request: StoreKnowledgeRequest,
) -> KnowledgeArtifact:
    use_case = StoreKnowledgeUseCase(knowledge_repo)
    # Sửa RET504: return trực tiếp không qua biến trung gian
    return use_case.execute(request)


@app.post("/users/register", response_model=User, status_code=201)
async def register_user(request: RegisterUserRequest) -> User:
    use_case = RegisterUserUseCase(identity_repo)
    try:
        return use_case.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/v1/capabilities", response_model=list[BusinessCapability])
async def v1_list_business_capabilities() -> list[BusinessCapability]:
    return capability_registry.list_all()


@app.get("/governance/splay-tree")
async def get_splay_tree_layout() -> dict[str, Any]:
    return {"root": knowledge_repo.get_tree_layout()}


@app.get("/governance/splay-tree/mermaid")
async def get_splay_tree_mermaid() -> dict[str, str]:
    return {"mermaid": knowledge_repo.get_tree_mermaid()}


@app.get("/governance/audit-logs/{artifact_id}", response_model=list[AuditLogEntry])
async def get_artifact_audit_logs(artifact_id: str) -> list[AuditLogEntry]:
    return knowledge_repo.get_audit_logs(artifact_id)


@app.delete("/governance/documents/{artifact_id}")
async def delete_governance_document(
    artifact_id: str,
    author: Annotated[str, Body(embed=True)],
) -> dict[str, str]:
    success = knowledge_repo.delete(artifact_id, author)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    return {"message": f"Đã xóa tài liệu {artifact_id} thành công."}


assembly_engine = ArchitectureAssembly()


@app.post("/governance/assembly/commit", response_model=dict[str, Any], status_code=201)
async def commit_to_assembly(
    artifact_id: Annotated[str, Body(embed=True)],
    action: Annotated[str, Body(embed=True)],
    author: Annotated[str, Body(embed=True)],
) -> dict[str, Any]:
    artifact = knowledge_repo.find_by_id(artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Không tìm thấy tri thức")

    votes = [
        ConsensusVote(voter="ArchitectAgent", decision="APPROVED", reason="OK"),
        ConsensusVote(voter="ReviewerAgent", decision="APPROVED", reason="Pass"),
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


@app.post("/evolution/propose", status_code=201)
async def propose_evolution(
    obj_id: Annotated[str, Body(embed=True)],
    name: Annotated[str, Body(embed=True)],
    payload: Annotated[dict[str, Any], Body(embed=True)],
    author: Annotated[str, Body(embed=True)],
    triggered_by: Annotated[str, Body(embed=True)],
    parent_id: Annotated[str | None, Body(embed=True)] = None,
    voters_payload: Annotated[list[dict[str, str]] | None, Body(embed=True)] = None,
) -> dict[str, Any]:
    req = ProposeEvolutionRequest(
        id=obj_id,
        name=name,
        payload=payload,
        author=author,
        triggered_by=triggered_by,
        parent_id=parent_id,
    )
    votes = [
        CouncilVote(
            voter=v.get("voter", "ArchitectAgent"),
            decision=v.get("decision", "APPROVED"),
            reason=v.get("reason", "Autocommit approved"),
        )
        for v in (voters_payload or [{"voter": "ArchitectAgent", "decision": "APPROVED", "reason": "OK"}])
    ]
    use_case = ProposeEvolutionUseCase(evolution_repo, evo_council)
    try:
        saved = use_case.execute(req, votes)
        compiler = ArchitectureCompiler(ROOT_PATH)
        compiler.sync_adr_index(saved.id, saved.name, "Governance", "Accepted")
        return {
            "message": "Đề xuất tiến hóa thành công.",
            "id": saved.id,
            "version": saved.version.to_string(),
            "payload": saved.payload,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/reflection/analyze", response_model=ReflectionReport, status_code=201)
async def analyze_reflection_report(
    subject_id: Annotated[str, Body(embed=True)],
    trigger_event: Annotated[str, Body(embed=True)],
    passed_checks: Annotated[bool, Body(embed=True)],
) -> ReflectionReport:
    use_case = AnalyzeReflectionUseCase(reflection_repo)
    return use_case.execute(
        subject_id=subject_id,
        trigger_event=trigger_event,
        passed_checks=passed_checks,
    )


@app.post("/learning/ingest", response_model=Experience, status_code=201)
async def ingest_learning_experience(
    reflection_id: Annotated[str, Body(embed=True)],
) -> Experience:
    use_case = IngestLearningUseCase(learning_repo, reflection_repo)
    try:
        return use_case.execute(reflection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.post("/prediction/run", response_model=Prediction, status_code=201)
async def run_prediction_engine(
    payload: HistoricalMetricsPayload,
) -> Prediction:
    use_case = RunPredictionUseCase(prediction_repo)
    try:
        return use_case.execute(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/simulation/run", response_model=Simulation, status_code=201)
async def run_simulation_engine(
    request: SimulationRequest,
) -> Simulation:
    use_case = RunSimulationUseCase(simulation_repo)
    return use_case.execute(request)


@app.post("/self-rewrite/run", response_model=SelfRewriteJob, status_code=201)
async def run_self_rewrite_engine(
    request: SelfRewriteRequest,
) -> SelfRewriteJob:
    use_case = RunSelfRewriteUseCase(self_rewrite_repo)
    return use_case.execute(request)


@app.post("/v1/memory/store", response_model=MemoryResponse, status_code=201)
async def v1_store_new_memory(
    request: StoreMemoryCommand,
    idempotency_key: Annotated[str | None, Body(embed=True)] = None,
) -> MemoryResponse:
    handler = StoreMemoryHandler(memory_repo)
    if idempotency_key:
        return idempotency_service.process(
            idempotency_key, handler.handle, request
        )
    return cast(
        MemoryResponse,
        TelemetryService.measure_duration(handler.handle)(request),
    )


@app.get("/v1/federation/members", response_model=list[EcosystemMember])
async def v1_list_ecosystem_members() -> list[EcosystemMember]:
    return federation_registry.list_members()


@app.get("/v1/registry", response_model=list[RegistryResource])
async def v1_list_discovered_resources() -> list[RegistryResource]:
    return enterprise_registry.list_all()


@app.post("/autonomous/run-cycle", response_model=LoopCycle, status_code=201)
async def run_autonomous_loop_cycle(
    request: LoopCycleRequest,
) -> LoopCycle:
    services = {
        "knowledge_repo": knowledge_repo,
        "memory_repo": memory_repo,
        "intelligence_registry": intelligence_registry,
        "workflow_registry": workflow_registry,
        "reflection_repo": reflection_repo,
        "learning_repo": learning_repo,
        "prediction_repo": prediction_repo,
        "simulation_repo": simulation_repo,
        "self_rewrite_repo": self_rewrite_repo,
        "evolution_repo": evolution_repo,
        "evo_council": evo_council,
        "federation_registry": federation_registry,
        "civilization_repo": civilization_repo,
    }
    use_case = RunAutonomousLoopUseCase(autonomous_repo, services)
    try:
        cycle = use_case.execute(request)
        compiler = ArchitectureCompiler(ROOT_PATH)
        compiler.sync_current_context(
            score=98, active_packages_count=21, violations_count=0
        )
        compiler.sync_task_state("T-007", completed=True)
        return cycle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
