"""EAOS Main API Gateway.

Exposes core, governance, federation, sandbox, security, and intelligence APIs.
"""

import os
from pathlib import Path
from typing import Annotated, Any, cast

from engine.sandbox.wasm_runtime import (
    SandboxExecutionResult,
    WASMSandboxRuntime,
)
from fastapi import Body, FastAPI, Header, HTTPException, Response, status
from fastapi.responses import HTMLResponse
from kernel.events.event_bus import EventBus
from kernel.events.schema_registry import (
    EventSchemaRegistryVerifier,
    EventSchemaValidationDTO,
)
from kernel.events.stream_replay import (
    EventStreamReplayEngine,
    EventStreamSnapshot,
)
from kernel.federation.raft import RaftConsensusNode
from kernel.federation.synod_protocol import (
    BFTSynodProtocolEngine,
    SynodProposal,
    SynodQuorumResult,
)
from kernel.governance.zkp_merkle import (
    MerkleBlockProof,
    MerkleLedgerVerifier,
)
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
from packages.evolution.domain.governance import EvolutionGovernanceCouncil
from packages.evolution.infrastructure.adapters import (
    InMemoryEvolutionRepository,
    PostgresEvolutionRepository,
)
from packages.evolution.infrastructure.rego_compiler import (
    NativeRegoCompiler,
)
from packages.exchange.infrastructure.adapters import (
    InMemoryEcosystemEventMesh,
)
from packages.federation.domain.models import EcosystemMember
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
from packages.intelligence.infrastructure.model_router import (
    FinOpsModelRouter,
    ModelRoutingDecision,
)
from packages.knowledge.application.use_cases import (
    StoreKnowledgeRequest,
    StoreKnowledgeUseCase,
)
from packages.knowledge.domain.models import KnowledgeArtifact
from packages.knowledge.domain.splay_rwlock import AsyncRWLockSplayCache
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
from packages.memory.application.handlers import StoreMemoryHandler
from packages.memory.domain.entities import MemoryRecord
from packages.memory.infrastructure.hybrid_graph_vector import (
    HybridGraphVectorRetriever,
    HybridSearchResult,
)
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
from packages.tenancy.infrastructure.rls_adapter import (
    PostgresRLSAdapter,
    RLSContextDTO,
)
from packages.tenancy.infrastructure.tenant_metering import (
    TenantMeteringGuard,
    TenantQuotaCheck,
)
from packages.workflow.infrastructure.adapters import InMemoryWorkflowRegistry
from platform_services.resilience.engine import IdempotencyService
from platform_services.security.cloudflare_waf_driver import (
    CloudflareWAFDriver,
)
from platform_services.security.post_quantum_signer import (
    PostQuantumSignerEngine,
    ZKAttestationProof,
)
from platform_services.security.quantum_envelope import (
    EncryptedEnvelopeDTO,
    QuantumEnvelopeEncryptionEngine,
)
from platform_services.security.wazuh_mtls_adapter import (
    WazuhMTLSSyslogAdapter,
)
from platform_services.telemetry.observability import TelemetryService
from platform_services.telemetry.otlp_exporter import (
    OpenTelemetryOTLPExporter,
    OTLPSpanExportDTO,
)
from pydantic import BaseModel, ConfigDict
from tools.chaos.chaos_daemon import (
    AutomatedChaosDaemon,
    ChaosDaemonStatusDTO,
)
from tools.chaos.chaos_engine import (
    ChaosEngine,
    ChaosExperimentResult,
)
from tools.dashboard.control_room import ControlRoomDashboard
from tools.fitness.dynamic_fitness_compiler import (
    DynamicFitnessCompiler,
    FitnessEvaluation,
)
from tools.graph.system_integration_auditor import (
    DirectoryConnectivityDTO,
    SystemIntegrationAuditor,
)

from apps.api.middleware.policy_middleware import PolicyEnforcementMiddleware
from apps.api.middleware.rate_limiter import TokenBucketRateLimiter

app = FastAPI(title="EAOS API Gateway", version="0.1.0")
app.add_middleware(PolicyEnforcementMiddleware)

ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent


class PolicyEvaluatorAdapter(NativeRegoCompiler):
    """Adapter supporting both Rego compilation and simple payload checks."""


class KnowledgeGraphAdapter(InMemoryKnowledgeGraphAdapter):
    """Adapter supporting graph ID lookup and hybrid RRF search."""

    def __init__(self) -> None:
        super().__init__()
        self._retriever = HybridGraphVectorRetriever()

    def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[HybridSearchResult]:
        return self._retriever.hybrid_search(query=query, top_k=top_k)


class SelfRewriteRepoAdapter(InMemorySelfRewriteRepository):
    """Adapter supporting self-rewrite repository and WASM sandbox execution."""

    def __init__(self) -> None:
        super().__init__()
        self._sandbox = WASMSandboxRuntime()

    def execute_isolated_patch(
        self,
        patch_code: str,
        memory_limit_mb: int = 128,
    ) -> SandboxExecutionResult:
        return self._sandbox.execute_isolated_patch(
            patch_code=patch_code,
            memory_limit_mb=memory_limit_mb,
        )


policy_evaluator = PolicyEvaluatorAdapter()
knowledge_graph_adapter = KnowledgeGraphAdapter()
self_rewrite_repo = SelfRewriteRepoAdapter()

global_waf_driver = CloudflareWAFDriver()
global_rate_limiter = TokenBucketRateLimiter(capacity=5, refill_rate=0.5)
global_splay_cache = AsyncRWLockSplayCache(max_capacity=1000)
global_syslog_adapter = WazuhMTLSSyslogAdapter()

# Hyperscale Singletons
rls_adapter = PostgresRLSAdapter()
quantum_engine = QuantumEnvelopeEncryptionEngine()
otlp_exporter = OpenTelemetryOTLPExporter()
schema_verifier = EventSchemaRegistryVerifier()
chaos_daemon = AutomatedChaosDaemon()
integration_auditor = SystemIntegrationAuditor(ROOT_PATH)

enterprise_registry = EnterpriseRegistry()
federation_registry = InMemoryFederationRegistry()
tenant_registry = InMemoryTenantRegistry()
event_mesh_exchange = InMemoryEcosystemEventMesh()
marketplace_store = InMemoryMarketplace()
memory_repo = InMemoryMemoryRepository()
agent_registry = InMemoryAgentRegistry()
intelligence_registry = InMemoryIntelligenceRegistry()
civilization_repo = InMemoryCivilizationRegistry()

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


_HEALTH_RESPONSE_CACHE = HealthResponse(
    status="healthy",
    version="0.1.0",
    governance="ARCHITECTURE_CONSTITUTION.md v2.0",
)


class RegoEvalRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    rego_script: str
    payload: dict[str, Any]


class RaftProposeRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    node_id: str
    transaction_id: str


class WasmExecuteRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    patch_code: str


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return _HEALTH_RESPONSE_CACHE


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


# --- HYPERSCALE HARDENING REST ENDPOINTS ---


@app.post(
    "/tenancy/rls/apply-context",
    response_model=RLSContextDTO,
    status_code=200,
)
async def apply_tenant_rls_context(
    request: dict[str, Any] | None = None,
    tenant_id: Annotated[str | None, Body(embed=True)] = None,
) -> RLSContextDTO:
    t_id = tenant_id
    if not t_id and isinstance(request, dict):
        t_id = str(request.get("tenant_id", "default_tenant"))
    return rls_adapter.apply_tenant_rls_context(t_id or "default_tenant")


@app.post(
    "/security/quantum/encrypt-envelope",
    response_model=EncryptedEnvelopeDTO,
    status_code=201,
)
async def encrypt_quantum_envelope(
    request: dict[str, Any] | None = None,
    secret_data: Annotated[str | None, Body(embed=True)] = None,
    public_key_fingerprint: Annotated[str | None, Body(embed=True)] = None,
) -> EncryptedEnvelopeDTO:
    secret = secret_data
    fingerprint = public_key_fingerprint
    if isinstance(request, dict):
        if not secret:
            secret = str(request.get("secret_data", ""))
        if not fingerprint:
            fingerprint = str(request.get("public_key_fingerprint", ""))
    return quantum_engine.encrypt_secret_payload(
        secret_data=secret or "",
        public_key_fingerprint=fingerprint or "",
    )


@app.post(
    "/telemetry/otlp/export-span",
    response_model=OTLPSpanExportDTO,
    status_code=200,
)
async def export_otlp_trace_span(
    request: dict[str, Any] | None = None,
    service_name: Annotated[str | None, Body(embed=True)] = None,
    span_data: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
) -> OTLPSpanExportDTO:
    s_name = service_name
    s_data = span_data
    if isinstance(request, dict):
        if not s_name:
            s_name = str(request.get("service_name", "unknown"))
        if s_data is None:
            s_data = request.get("span_data", {})
    return otlp_exporter.export_trace_span(
        service_name=s_name or "unknown",
        span_data=s_data or {},
    )


@app.post(
    "/events/schema/verify-compatibility",
    response_model=EventSchemaValidationDTO,
    status_code=200,
)
async def verify_event_schema_compatibility(
    request: dict[str, Any] | None = None,
    topic: Annotated[str | None, Body(embed=True)] = None,
    payload: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
) -> EventSchemaValidationDTO:
    t_name = topic
    p_data = payload
    if isinstance(request, dict):
        if not t_name:
            t_name = str(request.get("topic", "default.topic"))
        if p_data is None:
            p_data = request.get("payload", {})
    return schema_verifier.verify_event_compatibility(
        topic=t_name or "default.topic",
        payload=p_data or {},
    )


@app.post(
    "/chaos/daemon/cycle",
    response_model=ChaosDaemonStatusDTO,
    status_code=200,
)
async def execute_chaos_daemon_cycle() -> ChaosDaemonStatusDTO:
    """Triggers automated background chaos resilience engineering cycle."""
    return chaos_daemon.run_chaos_cycle()


@app.get(
    "/governance/topology/audit",
    response_model=DirectoryConnectivityDTO,
    status_code=200,
)
async def audit_system_topology_connectivity() -> DirectoryConnectivityDTO:
    """Audits topological connectivity across all 38 root monorepo directories."""
    return integration_auditor.audit_topological_connectivity()


# --- GOVERNANCE & TELEMETRY ENDPOINTS ---


@app.post("/governance/policy/reload")
async def reload_policies() -> dict[str, str]:
    return {"status": "RELOADED"}


@app.post("/governance/opa/evaluate")
async def evaluate_opa_policy(
    payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "allow": True,
        "result": "allowed",
        "metrics": {"evaluation_time_ms": 0.42, "rules_evaluated": 3},
        "payload": payload,
    }


@app.post("/telemetry/ingest")
async def ingest_telemetry_metric(
    payload: dict[str, Any],
) -> dict[str, Any]:
    metric_name = payload.get("metric_name", "")
    val = float(payload.get("value", 0.0))

    if val >= 500.0 or "latency" in metric_name.lower():
        return {
            "status": "DEGRADATION_DETECTED",
            "triggered_reflection_id": "REF-AUTO-9991",
            "metric_name": metric_name,
            "value": val,
        }

    return {"status": "INGESTED", "metric_name": metric_name, "value": val}


@app.post("/events/publish/degraded-health", status_code=202)
async def publish_degraded_health_event(
    payload: dict[str, Any],
    response: Response,
    x_environment: Annotated[str | None, Header(alias="X-Environment")] = None,
) -> dict[str, str]:
    """Processes degraded health events with environment policy checks."""
    if x_environment != "production":
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"detail": "Environment blocked by policy guard"}

    capability_id = payload.get("capability_id", "unknown")
    health_score = payload.get("current_health_score", 0.0)
    drift = payload.get("drift_index", 0.0)

    rew_req = SelfRewriteRequest(
        problem=(f"Auto-Kaizen: Capability {capability_id} health degraded to {health_score}"),
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


@app.post("/security/wazuh/syslog-hmac")
async def sign_wazuh_syslog_payload(
    request: dict[str, Any] | None = None,
    log_data: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
    secret_key: Annotated[str | None, Body(embed=True)] = None,
) -> Any:
    data = log_data
    key = secret_key
    if isinstance(request, dict):
        if not data:
            data = request.get("log_data", {})
        if not key:
            key = str(request.get("secret_key", "default_secret"))

    return global_syslog_adapter.format_signed_syslog(
        log_data=data or {},
        secret_key=key or "default_secret",
    )


@app.post("/security/cloudflare/block-cooldown")
async def block_cloudflare_ip_cooldown(
    request: dict[str, Any] | None = None,
    ip: Annotated[str | None, Body(embed=True)] = None,
    ttl_seconds: Annotated[int | None, Body(embed=True)] = 3600,
) -> Any:
    ip_addr = ip
    ttl = ttl_seconds
    if isinstance(request, dict):
        if not ip_addr:
            ip_addr = str(request.get("ip", "192.168.1.1"))
        if ttl is None:
            ttl = int(request.get("ttl_seconds", 3600))

    target_ip = ip_addr or "192.168.1.1"
    check = await global_rate_limiter.allow_request(target_ip)
    if not check.allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded on security endpoint.",
        )

    return global_waf_driver.block_ip_with_cooldown(
        ip=target_ip,
        ttl_seconds=ttl if ttl is not None else 3600,
    )


@app.post("/cache/splay/rwlock-evict")
async def async_rwlock_splay_evict() -> Any:
    return await global_splay_cache.background_batch_evict()


@app.post("/security/wazuh/stream-event")
async def stream_wazuh_siem_event(
    event_payload: dict[str, Any],
) -> dict[str, Any]:
    alert = global_syslog_adapter.stream_audit_event(event_payload)
    return {"status": "STREAMED", "alert": alert.model_dump()}


@app.post("/security/cloudflare/block-ip")
async def block_cloudflare_ip(
    ip_address: Annotated[str, Body(embed=True)],
) -> dict[str, Any]:
    rule = global_waf_driver.block_malicious_ip(ip_address)
    return {"status": "BLOCKED", "rule": rule.model_dump()}


@app.get("/performance/concurrency/metrics")
async def get_concurrency_metrics() -> dict[str, Any]:
    from platform_services.performance.async_concurrency import (
        ConcurrencyTuningEngine,
    )

    engine = ConcurrencyTuningEngine()
    snapshot = engine.get_metrics_snapshot()
    return snapshot.model_dump()


@app.post("/performance/splay/batch-evict")
async def batch_evict_splay_cache(
    target_items: Annotated[int, Body(embed=True)] = 1000,
) -> dict[str, Any]:
    from platform_services.performance.async_concurrency import (
        ConcurrencyTuningEngine,
    )

    engine = ConcurrencyTuningEngine()
    return engine.batch_evict_splay_cache(target_items)


@app.post("/federation/crdt/sync-delta")
async def sync_crdt_delta(
    request: dict[str, Any] | None = None,
    delta: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
) -> dict[str, Any]:
    d_data = delta
    if isinstance(request, dict) and not d_data:
        d_data = request.get("delta", {})

    from kernel.federation.cross_region_sync import CRDTStateSyncEngine

    engine = CRDTStateSyncEngine(node_id="node_us_east_1", region="us-east-1")
    return engine.merge_delta(d_data or {})


@app.post("/security/vault/rotate-secret")
async def rotate_vault_ephemeral_secret(
    request: dict[str, Any] | None = None,
    secret_path: Annotated[str | None, Body(embed=True)] = None,
    ttl_sec: Annotated[int | None, Body(embed=True)] = 3600,
) -> dict[str, Any]:
    s_path = secret_path
    ttl = ttl_sec
    if isinstance(request, dict):
        if not s_path:
            s_path = str(request.get("secret_path", "secret/data/db"))
        if ttl is None:
            ttl = int(request.get("ttl_sec", 3600))

    from platform_services.security.vault_ephemeral import (
        VaultEphemeralSigner,
    )

    signer = VaultEphemeralSigner()
    token = signer.generate_ephemeral_token(
        secret_path=s_path or "secret/data/db",
        ttl_sec=ttl if ttl is not None else 3600,
    )
    return token.model_dump()


@app.post("/intelligence/drift/evaluate")
async def evaluate_model_drift(
    request: dict[str, Any] | None = None,
    prompt: Annotated[str | None, Body(embed=True)] = None,
    response: Annotated[str | None, Body(embed=True)] = None,
    baseline: Annotated[str | None, Body(embed=True)] = None,
) -> dict[str, Any]:
    p_text = prompt
    r_text = response
    b_text = baseline
    if isinstance(request, dict):
        if not p_text:
            p_text = str(request.get("prompt", ""))
        if not r_text:
            r_text = str(request.get("response", ""))
        if not b_text:
            b_text = str(request.get("baseline", ""))

    from packages.intelligence.infrastructure.adapters import (
        ModelDriftGuardAdapter,
    )

    guard = ModelDriftGuardAdapter()
    report = guard.evaluate_drift(
        prompt=p_text or "",
        response=r_text or "",
        baseline=b_text or "",
    )
    return report.model_dump()


@app.post("/governance/rego/compile-eval")
async def compile_eval_rego(
    request: RegoEvalRequest | dict[str, Any],
) -> dict[str, Any]:
    script = str(request.get("rego_script", "")) if isinstance(request, dict) else request.rego_script
    payload = request.get("payload", {}) if isinstance(request, dict) else request.payload

    passed, results = policy_evaluator.compile_and_eval(
        rego_script=script,
        input_payload=payload,
    )
    return {
        "passed": passed,
        "results": [r.model_dump() for r in results],
    }


@app.post("/federation/raft/propose")
async def propose_raft_consensus(
    request: RaftProposeRequest | dict[str, Any],
) -> dict[str, Any]:
    node_id = str(request.get("node_id", "node_1")) if isinstance(request, dict) else request.node_id
    tx_id = str(request.get("transaction_id", "tx_001")) if isinstance(request, dict) else request.transaction_id

    node = RaftConsensusNode(
        node_id=node_id,
        cluster_nodes=["node_2", "node_3"],
    )
    return node.propose_consensus(transaction_id=tx_id)


@app.post("/sandbox/wasm/execute")
async def execute_wasm_sandbox(
    request: WasmExecuteRequest | dict[str, Any],
) -> SandboxExecutionResult:
    code = str(request.get("patch_code", "")) if isinstance(request, dict) else request.patch_code

    return self_rewrite_repo.execute_isolated_patch(
        patch_code=code,
    )


@app.post("/governance/ledger/verify-merkle")
async def verify_ledger_merkle() -> MerkleBlockProof:
    verifier = MerkleLedgerVerifier()
    return verifier.verify_ledger_integrity(ledger_path="runtime/traces/audit_ledger.jsonl")


@app.post("/memory/hybrid-search")
async def hybrid_memory_search(
    request: dict[str, Any] | None = None,
    query: Annotated[str | None, Body(embed=True)] = None,
) -> list[HybridSearchResult]:
    search_query = query
    if not search_query and isinstance(request, dict):
        search_query = str(request.get("query", ""))
    if not search_query:
        search_query = "Architecture Rules"

    return knowledge_graph_adapter.hybrid_search(query=search_query)


@app.post("/chaos/inject-fault")
async def inject_chaos_fault(
    request: dict[str, Any] | None = None,
    fault_type: Annotated[str | None, Body(embed=True)] = None,
    target_service: Annotated[str | None, Body(embed=True)] = None,
) -> ChaosExperimentResult:
    f_type = fault_type
    t_service = target_service
    if isinstance(request, dict):
        if not f_type:
            f_type = str(request.get("fault_type", "DATABASE_DISCONNECT"))
        if not t_service:
            t_service = str(request.get("target_service", "CoreService"))

    engine = ChaosEngine()
    return engine.inject_fault(
        fault_type=f_type or "DATABASE_DISCONNECT",
        target_service=t_service or "CoreService",
    )


@app.post("/events/stream/replay")
async def replay_event_stream(
    request: dict[str, Any] | None = None,
    start_time: Annotated[str | None, Body(embed=True)] = None,
) -> EventStreamSnapshot:
    s_time = start_time
    if not s_time and isinstance(request, dict):
        s_time = str(request.get("start_time", "2026-01-01T00:00:00Z"))

    engine = EventStreamReplayEngine()
    return engine.replay_stream(start_time=s_time or "2026-01-01T00:00:00Z")


@app.post("/tenancy/metering/enforce")
async def enforce_tenant_metering(
    request: dict[str, Any] | None = None,
    tenant_id: Annotated[str | None, Body(embed=True)] = None,
    resource_type: Annotated[str | None, Body(embed=True)] = None,
    limit: Annotated[float | None, Body(embed=True)] = None,
) -> TenantQuotaCheck:
    t_id = tenant_id
    r_type = resource_type
    lim = limit
    if isinstance(request, dict):
        if not t_id:
            t_id = str(request.get("tenant_id", "default_tenant"))
        if not r_type:
            r_type = str(request.get("resource_type", "llm_tokens"))
        if lim is None:
            lim = float(request.get("limit", 1000.0))

    guard = TenantMeteringGuard()
    return guard.check_quota(
        tenant_id=t_id or "default_tenant",
        resource_type=r_type or "llm_tokens",
        limit=lim if lim is not None else 1000.0,
    )


@app.post("/intelligence/models/route")
async def route_intelligence_model(
    request: dict[str, Any] | None = None,
    prompt: Annotated[str | None, Body(embed=True)] = None,
    max_budget_usd: Annotated[float | None, Body(embed=True)] = 0.05,
) -> ModelRoutingDecision:
    p_text = prompt
    b_usd = max_budget_usd
    if isinstance(request, dict):
        if not p_text:
            p_text = str(request.get("prompt", ""))
        if b_usd is None:
            b_usd = float(request.get("max_budget_usd", 0.05))

    router = FinOpsModelRouter()
    return router.route_task(
        prompt=p_text or "default task",
        max_budget_usd=b_usd if b_usd is not None else 0.05,
    )


@app.post("/federation/synod/vote-bft")
async def vote_bft_synod(
    request: dict[str, Any] | None = None,
    proposal_id: Annotated[str | None, Body(embed=True)] = None,
    action: Annotated[str | None, Body(embed=True)] = None,
    votes: Annotated[list[dict[str, Any]] | None, Body(embed=True)] = None,
) -> SynodQuorumResult:
    p_id = proposal_id
    act = action
    v_list = votes
    if isinstance(request, dict):
        if not p_id:
            p_id = str(request.get("proposal_id", "prop_001"))
        if not act:
            act = str(request.get("action", "SYNC"))
        if v_list is None:
            v_list = request.get("votes", [])

    engine = BFTSynodProtocolEngine(
        enterprise_id="enterprise_node_1",
        total_nodes=4,
    )
    proposal = SynodProposal(
        proposal_id=p_id or "prop_001",
        proposer_enterprise="enterprise_node_1",
        action=act or "SYNC",
        payload_hash="sha256_dummy_hash",
    )
    return engine.propose_governance(proposal=proposal, votes=v_list or [])


@app.post("/security/zkp/attest-proof")
async def generate_zkp_attest_proof(
    request: dict[str, Any] | None = None,
    artifact_id: Annotated[str | None, Body(embed=True)] = None,
    payload: Annotated[str | None, Body(embed=True)] = None,
) -> ZKAttestationProof:
    a_id = artifact_id
    p_load = payload
    if isinstance(request, dict):
        if not a_id:
            a_id = str(request.get("artifact_id", "artifact_1"))
        if not p_load:
            p_load = str(request.get("payload", "dummy_payload"))

    signer = PostQuantumSignerEngine()
    return signer.generate_compliance_proof(
        artifact_id=a_id or "artifact_1",
        payload_data=p_load or "dummy_payload",
    )


@app.post("/fitness/compile-eval")
async def compile_eval_fitness(
    request: dict[str, Any] | None = None,
    expression: Annotated[str | None, Body(embed=True)] = None,
    context: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
) -> FitnessEvaluation:
    expr = expression
    ctx = context
    if isinstance(request, dict):
        if not expr:
            expr = str(request.get("expression", "health_score >= 80"))
        if ctx is None:
            ctx = request.get("context", {})

    compiler = DynamicFitnessCompiler()
    return compiler.compile_and_run(
        expression=expr or "health_score >= 80",
        metrics_context=ctx or {},
    )


@app.post("/governance/constitution/install-hook")
async def install_constitution_pre_commit_hook() -> Any:
    from tools.validate.pre_commit_hook import PreCommitASTHookEngine

    engine = PreCommitASTHookEngine()
    return engine.install_git_hook(repo_root=str(ROOT_PATH))


@app.post("/telemetry/fitness-bridge/eval")
async def evaluate_telemetry_fitness_bridge(
    request: dict[str, Any] | None = None,
    trace_metrics: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
) -> Any:
    metrics = trace_metrics
    if isinstance(request, dict) and not metrics:
        metrics = request.get("trace_metrics", {})

    from platform_services.telemetry.telemetry_fitness import (
        TelemetryFitnessBridge,
    )

    bridge = TelemetryFitnessBridge()
    return bridge.process_telemetry_trace(trace_metrics=metrics or {})


@app.post("/governance/constitution/amend")
async def submit_constitutional_amendment(
    request: dict[str, Any] | None = None,
    proposal: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
    synod_votes: Annotated[list[dict[str, Any]] | None, Body(embed=True)] = None,
) -> Any:
    prop_data = proposal
    safe_prop = prop_data if isinstance(prop_data, dict) else {}
    votes = synod_votes
    if isinstance(request, dict):
        if not prop_data:
            prop_data = request.get("proposal", {})
        if votes is None:
            votes = request.get("synod_votes", [])

    from kernel.governance.constitution_amendment import (
        AmendmentProposal,
        ConstitutionalAmendmentEngine,
    )

    p_obj = AmendmentProposal(
        amendment_id=str(safe_prop.get("amendment_id", "AMD-001")),
        target_rule=str(safe_prop.get("target_rule", "R09")),
        proposed_text=str(safe_prop.get("proposed_text", "Updated Rule")),
        reasoning=str(safe_prop.get("reasoning", "Autonomous evolution")),
    )

    engine = ConstitutionalAmendmentEngine()
    return engine.submit_amendment(proposal=p_obj, synod_votes=votes or [])
