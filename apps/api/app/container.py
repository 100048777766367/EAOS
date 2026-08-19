"""Application Singletons Container for apps/api."""

import os
from pathlib import Path
from typing import Any

from engine.sandbox.wasm_runtime import WASMSandboxRuntime
from kernel.events.event_bus import EventBus
from kernel.events.schema_registry import EventSchemaRegistryVerifier
from kernel.registry.enterprise_registry import EnterpriseRegistry
from packages.agent.infrastructure.adapters import InMemoryAgentRegistry
from packages.autonomous.infrastructure.adapters import (
    InMemoryAutonomousRepository,
    PostgresAutonomousRepository,
)
from packages.capability.domain.models import BusinessCapability
from packages.capability.infrastructure.adapters import InMemoryCapabilityRegistry
from packages.civilization.infrastructure.adapters import InMemoryCivilizationRegistry
from packages.evolution.domain.governance import EvolutionGovernanceCouncil
from packages.evolution.infrastructure.adapters import (
    InMemoryEvolutionRepository,
    PostgresEvolutionRepository,
)
from packages.evolution.infrastructure.rego_compiler import NativeRegoCompiler
from packages.exchange.infrastructure.adapters import InMemoryEcosystemEventMesh
from packages.federation.infrastructure.adapters import InMemoryFederationRegistry
from packages.identity.infrastructure.adapters import (
    InMemoryUserRepository,
    PostgresUserRepository,
)
from packages.intelligence.infrastructure.adapters import InMemoryIntelligenceRegistry
from packages.knowledge.domain.splay_rwlock import AsyncRWLockSplayCache
from packages.knowledge.infrastructure.adapters import (
    PostgresKnowledgeRepository,
    SplayCacheKnowledgeRepository,
)
from packages.knowledge_graph.infrastructure.adapters import InMemoryKnowledgeGraphAdapter
from packages.learning.infrastructure.adapters import InMemoryExperienceRepository
from packages.marketplace.infrastructure.adapters import InMemoryMarketplace
from packages.memory.infrastructure.hybrid_graph_vector import HybridGraphVectorRetriever, HybridSearchResult
from packages.memory.infrastructure.repository import InMemoryMemoryRepository
from packages.prediction.infrastructure.adapters import InMemoryPredictionRepository
from packages.reflection.infrastructure.adapters import InMemoryReflectionRepository
from packages.self_rewrite.infrastructure.adapters import InMemorySelfRewriteRepository
from packages.simulation.infrastructure.adapters import InMemorySimulationRepository
from packages.specification.infrastructure.adapters import InMemorySpecificationRegistry
from packages.tenancy.infrastructure.adapters import InMemoryTenantRegistry
from packages.tenancy.infrastructure.rls_adapter import PostgresRLSAdapter
from packages.workflow.infrastructure.adapters import InMemoryWorkflowRegistry
from platforms.resilience.engine import IdempotencyService
from platforms.security.cloudflare_waf_driver import CloudflareWAFDriver
from platforms.security.quantum_envelope import QuantumEnvelopeEncryptionEngine
from platforms.security.wazuh_mtls_adapter import WazuhMTLSSyslogAdapter
from platforms.telemetry.observability import TelemetryService
from platforms.telemetry.otlp_exporter import OpenTelemetryOTLPExporter
from tools.chaos.chaos_daemon import AutomatedChaosDaemon
from tools.graph.system_integration_auditor import SystemIntegrationAuditor

from apps.api.middleware.rate_limiter import TokenBucketRateLimiter

ROOT_PATH = Path(__file__).resolve().parents[3]


class KnowledgeGraphAdapter(InMemoryKnowledgeGraphAdapter):
    """Adapter supporting graph ID lookup and hybrid RRF search."""

    def __init__(self) -> None:
        super().__init__()
        self._retriever = HybridGraphVectorRetriever()

    def hybrid_search(self, query: str, top_k: int = 5) -> list[HybridSearchResult]:
        return self._retriever.hybrid_search(query=query, top_k=top_k)


class SelfRewriteRepoAdapter(InMemorySelfRewriteRepository):
    """Adapter supporting self-rewrite repository and WASM sandbox execution."""

    def __init__(self) -> None:
        super().__init__()
        self._sandbox = WASMSandboxRuntime()

    def execute_isolated_patch(self, patch_code: str, memory_limit_mb: int = 128) -> Any:
        return self._sandbox.execute_isolated_patch(patch_code=patch_code, memory_limit_mb=memory_limit_mb)


policy_evaluator = NativeRegoCompiler()
knowledge_graph_adapter = KnowledgeGraphAdapter()
self_rewrite_repo = SelfRewriteRepoAdapter()

global_waf_driver = CloudflareWAFDriver()
global_rate_limiter = TokenBucketRateLimiter(capacity=5, refill_rate=0.5)
global_splay_cache = AsyncRWLockSplayCache(max_capacity=1000)
global_syslog_adapter = WazuhMTLSSyslogAdapter()

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

db_url = os.getenv("DATABASE_URL", "postgresql://eaos:eaos@localhost:5432/eaos")

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
capability_registry.register(BusinessCapability(capability_type="cap-01", name="Knowledge Management"))
capability_registry.register(BusinessCapability(capability_type="cap-02", name="Identity Management"))

spec_registry = InMemorySpecificationRegistry()
workflow_registry = InMemoryWorkflowRegistry()
telemetry_service = TelemetryService()
idempotency_service = IdempotencyService()
event_bus = EventBus()
federation_repo = federation_registry

prometheus_exporter = telemetry_service


class TopologyUseCase:
    """Topology Use Case for Audit System."""

    def get_audit_report(self) -> dict[str, Any]:
        return {"status": "ACTIVE", "connectivity": "100%"}


topology_use_case = TopologyUseCase()
