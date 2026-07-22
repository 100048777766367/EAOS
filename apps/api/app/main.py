"""EAOS Main API Gateway."""

import os
from pathlib import Path
from typing import Annotated, Any, cast

from fastapi import Body, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from kernel.events.event_bus import EventBus
from kernel.registry.enterprise_registry import EnterpriseRegistry
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
from packages.evolution.domain.governance import (
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
from packages.knowledge.domain.models import KnowledgeArtifact
from packages.knowledge.infrastructure.adapters import (
    PostgresKnowledgeRepository,
    SplayCacheKnowledgeRepository,
)
from packages.knowledge_graph.application.dto import (
    IngestGraphBatchCommand,
    NodeIngestDTO,
)
from packages.knowledge_graph.application.use_cases import (
    IngestKnowledgeGraphUseCase,
)
from packages.knowledge_graph.domain.models import NodeType
from packages.knowledge_graph.infrastructure.adapters import (
    InMemoryKnowledgeGraphAdapter,
)
from packages.learning.infrastructure.adapters import (
    InMemoryExperienceRepository,
)
from packages.marketplace.infrastructure.adapters import InMemoryMarketplace
from packages.memory.application.dto import MemoryResponse, StoreMemoryCommand
from packages.memory.application.handlers import (
    StoreMemoryHandler,
)
from packages.memory.domain.entities import MemoryRecord
from packages.memory.infrastructure.repository import InMemoryMemoryRepository
from packages.prediction.infrastructure.adapters import (
    InMemoryPredictionRepository,
)
from packages.reflection.application.use_cases import AnalyzeReflectionUseCase
from packages.reflection.domain.models import ReflectionReport
from packages.reflection.infrastructure.adapters import (
    InMemoryReflectionRepository,
)
from packages.self_rewrite.application.dto import SelfRewriteRequest
from packages.self_rewrite.application.use_cases import RunSelfRewriteUseCase
from packages.self_rewrite.domain.models import SelfRewriteJob
from packages.self_rewrite.infrastructure.adapters import (
    InMemorySelfRewriteRepository,
)
from packages.simulation.infrastructure.adapters import (
    InMemorySimulationRepository,
)
from packages.specification.infrastructure.adapters import (
    InMemorySpecificationRegistry,
)
from packages.tenancy.infrastructure.adapters import InMemoryTenantRegistry
from packages.workflow.infrastructure.adapters import InMemoryWorkflowRegistry
from platform_services.resilience.engine import IdempotencyService
from platform_services.telemetry.observability import TelemetryService
from pydantic import BaseModel
from tools.dashboard.control_room import ControlRoomDashboard

from apps.api.middleware.policy_middleware import PolicyEnforcementMiddleware

app = FastAPI(title="EAOS API Gateway", version="0.1.0")
app.add_middleware(PolicyEnforcementMiddleware)

ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent

enterprise_registry = EnterpriseRegistry()
federation_registry = InMemoryFederationRegistry()
tenant_registry = InMemoryTenantRegistry()
event_mesh_exchange = InMemoryEcosystemEventMesh()
marketplace_store = InMemoryMarketplace()
memory_repo = InMemoryMemoryRepository()
agent_registry = InMemoryAgentRegistry()
intelligence_registry = InMemoryIntelligenceRegistry()
civilization_repo = InMemoryCivilizationRegistry()
knowledge_graph_adapter = InMemoryKnowledgeGraphAdapter()

db_url = os.getenv(
    "DATABASE_URL",
    "postgresql://eaos:eaos@localhost:5432/eaos",
)

try:
    postgres_knowledge_repo = PostgresKnowledgeRepository(db_url)
    knowledge_repo = SplayCacheKnowledgeRepository(postgres_knowledge_repo)
    identity_repo: Any = PostgresUserRepository(db_url)
    evolution_repo: Any = PostgresEvolutionRepository(db_url)
    autonomous_repo: Any = PostgresAutonomousRepository(db_url)
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
event_bus = EventBus()


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


@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard() -> HTMLResponse:
    dashboard = ControlRoomDashboard(ROOT_PATH)
    return HTMLResponse(content=dashboard.render_html())


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


@app.get("/v1/capabilities", response_model=list[BusinessCapability])
async def v1_list_capabilities() -> list[BusinessCapability]:
    return capability_registry.list_all()


@app.get("/v1/memory", response_model=list[MemoryRecord])
async def v1_list_memories() -> list[MemoryRecord]:
    return memory_repo.list_all()


@app.post("/v1/memory/store", response_model=MemoryResponse, status_code=201)
async def v1_store_memory(
    body: dict[str, Any],
) -> MemoryResponse:
    req_data = body.get("request", body)
    idem_key = body.get("idempotency_key")

    cmd = StoreMemoryCommand(
        decision_id=req_data.get("decision_id", "PR-01"),
        outcome=req_data.get("outcome", "SUCCESS"),
        evidence_summary=req_data.get("evidence_summary", ""),
        lesson_learned=req_data.get("lesson_learned", ""),
        key_learnings=req_data.get("key_learnings", []),
    )
    handler = StoreMemoryHandler(memory_repo)
    if idem_key:
        return cast(
            MemoryResponse,
            idempotency_service.process(idem_key, handler.handle, cmd),
        )
    return handler.handle(cmd)


@app.get("/v1/federation/members", response_model=list[EcosystemMember])
async def v1_list_federation_members() -> list[EcosystemMember]:
    return federation_registry.list_members()


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


@app.post("/self-rewrite/run", response_model=SelfRewriteJob, status_code=201)
async def run_self_rewrite_engine(
    request: SelfRewriteRequest,
) -> SelfRewriteJob:
    use_case = RunSelfRewriteUseCase(self_rewrite_repo)
    return use_case.execute(request)


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
        return use_case.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/events/publish/degraded-health", status_code=202)
async def publish_degraded_health_event(
    payload: dict[str, Any],
    x_environment: Annotated[str | None, Header(alias="X-Environment")] = None,
) -> dict[str, str]:
    capability_id = payload.get("capability_id", "unknown")
    health_score = payload.get("current_health_score", 0.0)
    drift = payload.get("drift_index", 0.0)

    rew_req = SelfRewriteRequest(
        problem=f"Auto-Kaizen: Capability {capability_id} health degraded to {health_score}",
        author="KaizenAutoEngine",
    )
    self_rewrite_use_case = RunSelfRewriteUseCase(self_rewrite_repo)
    self_rewrite_use_case.execute(rew_req)

    cmd = IngestGraphBatchCommand(
        graph_id="GLOBAL-GRAPH",
        nodes=[
            NodeIngestDTO(
                node_id=f"INC-{capability_id}",
                node_type=NodeType.INCIDENT,
                label=f"Incident: {capability_id}",
                name=f"Incident: {capability_id}",
                properties={"health_score": health_score, "drift_index": drift},
            )
        ],
        edges=[],
    )
    kg_use_case = IngestKnowledgeGraphUseCase(knowledge_graph_adapter)
    kg_use_case.execute(cmd)

    return {"status": "accepted"}
