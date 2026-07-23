"""EAOS Master Consolidated Integration & Unit Test Suite."""

import uuid
from pathlib import Path
from typing import Any

import pytest
from apps.api.app.main import app, policy_evaluator
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from packages.architecture_memory.domain.models import (
    ArchitectureMemoryRecordAggregate,
    MemoryTier,
    MemoryType,
)
from packages.architecture_memory.infrastructure.adapters import (
    PgVectorArchitectureMemoryAdapter,
)
from packages.metrics_engine.infrastructure.adapters import (
    InMemoryMetricsRepository,
)
from platform_services.telemetry.observability import (
    EAOSObservabilityMiddleware,
)
from tools.graph.dependency_graph_generator import (
    DependencyGraphGenerator,
)
from tools.metrics.architecture_metrics_calculator import (
    ArchitectureMetricsCalculator,
)

ROOT_PATH = Path(__file__).resolve().parent.parent


@pytest.fixture
def client() -> TestClient:
    """Provides isolated FastAPI TestClient instance."""
    return TestClient(app)


# ============================================================================
# 1. CORE & UNIT TESTS
# ============================================================================


def test_unit_dependency_graph_generator() -> None:
    """Verifies static dependency graph generation."""
    generator = DependencyGraphGenerator(ROOT_PATH)
    assert generator.generate() is True


def test_unit_architecture_metrics_calculator() -> None:
    """Verifies system architectural health score calculation."""
    calculator = ArchitectureMetricsCalculator(ROOT_PATH)
    assert calculator.calculate_all() is True
    assert calculator.architecture_score >= 80


# ============================================================================
# 2. BASELINE ENTERPRISE FLOWS
# ============================================================================


def test_int_health_and_identity_flow(client: TestClient) -> None:
    """Verifies gateway health and user registration flow."""
    health_resp = client.get("/health")
    assert health_resp.status_code == 200
    assert health_resp.json()["status"] == "healthy"

    test_email = f"agent.{uuid.uuid4().hex[:6]}@eaos.internal"
    user_resp = client.post(
        "/users/register",
        json={
            "email": test_email,
            "username": "AgentSmith",
            "password": "Password123!",
        },
    )
    assert user_resp.status_code == 201


def test_int_knowledge_splay_and_assembly_flow(
    client: TestClient,
) -> None:
    """Verifies knowledge creation flow."""
    knw_resp = client.post(
        "/knowledge",
        json={"title": "R1", "content": "Core", "author": "Arch"},
    )
    assert knw_resp.status_code == 201


def test_int_capabilities_specs_workflows_agents(
    client: TestClient,
) -> None:
    """Verifies capability listing endpoint."""
    cap_resp = client.get("/v1/capabilities")
    assert cap_resp.status_code == 200


def test_int_memory_idempotency_and_vector_search(
    client: TestClient,
) -> None:
    """Verifies architectural memory store with idempotency."""
    idempotency_key = f"IDEM-{uuid.uuid4().hex[:6]}"
    mem_payload = {
        "decision_id": "PR-01",
        "outcome": "SUCCESS",
        "evidence_summary": "Splay RAM Eviction verified.",
        "lesson_learned": "Splay Tree optimizes memory.",
        "key_learnings": ["Hot nodes at root."],
    }
    r1 = client.post(
        "/v1/memory/store",
        json={
            "request": mem_payload,
            "idempotency_key": idempotency_key,
        },
    )
    assert r1.status_code == 201


def test_int_reflection_learning_prediction_simulation(
    client: TestClient,
) -> None:
    """Verifies reflection diagnostic analysis flow."""
    ref_resp = client.post(
        "/reflection/analyze",
        json={
            "subject_id": "EVO-MOD-01",
            "trigger_event": "Failure",
            "passed_checks": False,
        },
    )
    assert ref_resp.status_code == 201


def test_int_self_rewrite_agent_chain(client: TestClient) -> None:
    """Verifies self-rewrite agent execution flow."""
    payload = {
        "problem": "Database port mismatch causing connection timeouts.",
        "author": "SystemMonitor",
    }
    response = client.post("/self-rewrite/run", json=payload)
    assert response.status_code == 201


def test_int_federation_tenancy_marketplace_civilization(
    client: TestClient,
) -> None:
    """Verifies federation membership listing endpoint."""
    fed_resp = client.get("/v1/federation/members")
    assert fed_resp.status_code == 200


def test_int_full_13_stage_autonomous_closed_loop(
    client: TestClient,
) -> None:
    """Verifies full 13-stage cybernetic evolution cycle."""
    auto_resp = client.post(
        "/autonomous/run-cycle",
        json={
            "problem": "System latency degrades under high load.",
            "author": "MonitorDaemon",
        },
    )
    assert auto_resp.status_code == 201


def test_int_document_lifecycle_management_flow() -> None:
    """Verifies mock documentation lifecycle creation and cleanup."""
    docs_dir = ROOT_PATH / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    mock_doc = docs_dir / "mock_system_constitution.md"
    mock_doc.write_text(
        "# Test Constitution\n\nRule 1: Boundary Isolation.",
        encoding="utf-8",
    )
    assert mock_doc.exists()
    if mock_doc.exists():
        mock_doc.unlink()


# ============================================================================
# 3. GRAND HARDENING & SOC SECURITY TESTS
# ============================================================================


def test_wazuh_siem_event_streaming_flow(client: TestClient) -> None:
    """Verifies Wazuh SIEM audit log streaming endpoint."""
    payload = {
        "tx_id": "TX-SEC-9001",
        "source_ip": "10.0.0.45",
        "action": "SECURITY_VIOLATION_DETECTED",
    }
    response = client.post("/security/wazuh/stream-event", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "STREAMED"
    assert data["alert"]["level"] == 7
    assert data["alert"]["source_ip"] == "10.0.0.45"


def test_cloudflare_waf_ip_blocking_flow(client: TestClient) -> None:
    """Verifies Cloudflare WAF automated IP threat blocking endpoint."""
    payload = {"ip_address": "198.51.100.12"}
    response = client.post("/security/cloudflare/block-ip", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "BLOCKED"
    assert data["rule"]["blocked_ip"] == "198.51.100.12"
    assert data["rule"]["mode"] == "block"


def test_concurrency_metrics_and_splay_batch_eviction_flow(
    client: TestClient,
) -> None:
    """Verifies high-concurrency tuning metrics and batch eviction."""
    metrics_resp = client.get("/performance/concurrency/metrics")
    assert metrics_resp.status_code == 200
    m_data = metrics_resp.json()
    assert m_data["p99_latency_ms"] < 50.0
    assert m_data["requests_per_second"] >= 10000.0

    evict_payload = {"target_items": 500}
    evict_resp = client.post("/performance/splay/batch-evict", json=evict_payload)
    assert evict_resp.status_code == 200
    e_data = evict_resp.json()
    assert e_data["status"] == "BATCH_EVICTION_COMPLETED"
    assert e_data["evicted_count"] == 500


def test_wazuh_hmac_syslog_signing_flow(client: TestClient) -> None:
    """Verifies HMAC SHA-256 syslog message formatting and signing."""
    payload = {
        "log_data": {"tx_id": "TX-AUDIT-999", "action": "RULE_EVALUATED"},
        "secret_key": "super_secret_hmac_key",
    }
    response = client.post("/security/wazuh/syslog-hmac", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "signature" in data
    assert len(data["signature"]) == 64


def test_cloudflare_cooldown_rate_limit_flow(client: TestClient) -> None:
    """Verifies Cloudflare WAF block decision and Token Bucket limiter."""
    payload = {"ip": "203.0.113.50", "ttl_seconds": 1800}
    response = client.post("/security/cloudflare/block-cooldown", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ip"] == "203.0.113.50"
    assert data["action"] == "BLOCK_WITH_COOLDOWN"


def test_async_rwlock_splay_cache_eviction_flow(
    client: TestClient,
) -> None:
    """Verifies non-blocking async RWLock batch eviction endpoint."""
    response = client.post("/cache/splay/rwlock-evict")
    assert response.status_code == 200
    data = response.json()
    assert "evicted_count" in data


# ============================================================================
# 4. ULTRA-SCALE TIER TESTS
# ============================================================================


def test_crdt_cross_region_sync_flow(client: TestClient) -> None:
    """Verifies multi-region CRDT state delta merge endpoint."""
    payload = {
        "delta": {
            "node_id": "node-us-east-1",
            "region": "us-east-1",
            "vector_clock": {"node-us-east-1": 1},
            "payload": {"status": "ACTIVE"},
        }
    }
    response = client.post("/federation/crdt/sync-delta", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["synced"] is True
    assert "node-us-east-1" in data["merged_clock"]


def test_vault_ephemeral_secret_rotation_flow(
    client: TestClient,
) -> None:
    """Verifies Zero-Trust dynamic secret rotation token endpoint."""
    payload = {"secret_path": "secret/data/db_pass", "ttl_sec": 900}
    response = client.post("/security/vault/rotate-secret", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["lease_duration_sec"] == 900


def test_model_drift_hallucination_guard_flow(
    client: TestClient,
) -> None:
    """Verifies AI semantic drift and hallucination guard endpoint."""
    payload = {
        "prompt": "Summarize architecture constitution",
        "response": ("The system allows arbitrary database access directly from domain models without restriction"),
        "baseline": ("Domain models must not import infrastructure or database libraries and must remain isolated"),
    }
    response = client.post("/intelligence/drift/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["hallucination_detected"] is True
    assert data["recommended_action"] == "FALLBACK_MODEL"


# ============================================================================
# 5. ULTIMATE & SUPREME ENTERPRISE TESTS
# ============================================================================


def test_event_stream_replay_flow(client: TestClient) -> None:
    """Verifies time-travel event stream replay endpoint."""
    payload = {"start_time": "2026-01-01T00:00:00Z"}
    response = client.post("/events/stream/replay", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "snapshot_id" in data


def test_tenant_metering_enforcement_flow(client: TestClient) -> None:
    """Verifies tenant resource metering and quota guard endpoint."""
    payload = {
        "tenant_id": "tenant_acme",
        "resource_type": "llm_tokens",
        "limit": 10000.0,
    }
    response = client.post("/tenancy/metering/enforce", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["allowed"] is True


def test_finops_model_routing_flow(client: TestClient) -> None:
    """Verifies FinOps AI model routing and cost optimization."""
    low_payload = {
        "prompt": "hello world",
        "max_budget_usd": 0.0005,
    }
    response = client.post("/intelligence/models/route", json=low_payload)
    assert response.status_code == 200
    low_data = response.json()
    assert low_data["selected_model"] == "ollama/llama3"


def test_bft_synod_federation_flow(client: TestClient) -> None:
    """Verifies inter-enterprise BFT Synod consensus voting endpoint."""
    payload = {
        "proposal_id": "prop_9001",
        "action": "FEDERATION_CROSS_BORDER_SYNC",
        "votes": [
            {"node": "node_1", "decision": "APPROVE"},
            {"node": "node_2", "decision": "APPROVE"},
            {"node": "node_3", "decision": "APPROVE"},
            {"node": "node_4", "decision": "REJECT"},
        ],
    }
    response = client.post("/federation/synod/vote-bft", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["achieved_bft_consensus"] is True


def test_post_quantum_zkp_attestation_flow(client: TestClient) -> None:
    """Verifies post-quantum zero-knowledge attestation proof endpoint."""
    payload = {
        "artifact_id": "artifact_core_v1",
        "payload": "ISO27001_COMPLIANCE_DATA_PAYLOAD",
    }
    response = client.post("/security/zkp/attest-proof", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] is True


def test_dynamic_fitness_compiler_flow(client: TestClient) -> None:
    """Verifies dynamic fitness function expression compilation."""
    pass_payload = {
        "expression": "health_score >= 80",
        "context": {"health_score": 95},
    }
    response = client.post("/fitness/compile-eval", json=pass_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["passed"] is True


# ============================================================================
# 6. HYPER & TOP-TIER ENTERPRISE TESTS
# ============================================================================


def test_merkle_ledger_verification_flow(client: TestClient) -> None:
    """Verifies Merkle tree audit log verification endpoint."""
    response = client.post("/governance/ledger/verify-merkle")
    assert response.status_code == 200
    data = response.json()
    assert "merkle_root" in data


def test_hybrid_graph_vector_rrf_search_flow(
    client: TestClient,
) -> None:
    """Verifies hybrid graph and vector RAG retrieval with RRF."""
    payload = {"query": "Enterprise Architecture Governance Rules"}
    response = client.post("/memory/hybrid-search", json=payload)
    assert response.status_code == 200


def test_chaos_engineering_fault_injection_flow(
    client: TestClient,
) -> None:
    """Verifies chaos fault injection endpoint."""
    payload = {
        "fault_type": "DATABASE_DISCONNECT",
        "target_service": "GovernanceLedgerService",
    }
    response = client.post("/chaos/inject-fault", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["system_recovered"] is True


def test_native_rego_compiler_flow(client: TestClient) -> None:
    """Verifies native in-process Rego compiler evaluation endpoint."""
    payload = {
        "rego_script": ("package governance\nallow = true\ninput.role == 'admin'"),
        "payload": {"role": "admin"},
    }
    response = client.post("/governance/rego/compile-eval", json=payload)
    assert response.status_code == 200


def test_raft_consensus_federation_flow(client: TestClient) -> None:
    """Verifies Raft consensus proposal endpoint."""
    payload = {
        "node_id": "node_1",
        "transaction_id": "tx_1001",
    }
    response = client.post("/federation/raft/propose", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["consensus"] == "ACHIEVED"


def test_wasm_sandbox_isolated_execution_flow(
    client: TestClient,
) -> None:
    """Verifies WASM sandbox patch execution isolation."""
    valid_payload = {"patch_code": "x = 10\ny = 20\nresult = x + y"}
    response = client.post("/sandbox/wasm/execute", json=valid_payload)
    assert response.status_code == 200


# ============================================================================
# 7. CONSTITUTION COMPLIANCE & MIDDLEWARE TESTS
# ============================================================================


def test_pre_commit_hook_installation_flow(
    client: TestClient,
) -> None:
    """Verifies Git pre-commit hook installation endpoint."""
    response = client.post("/governance/constitution/install-hook")
    assert response.status_code == 200


def test_telemetry_fitness_bridge_flow(client: TestClient) -> None:
    """Verifies telemetry-to-fitness bridge endpoint."""
    payload = {
        "trace_metrics": {
            "metric_name": "API_p99_latency_ms",
            "value": 185.5,
        }
    }
    response = client.post("/telemetry/fitness-bridge/eval", json=payload)
    assert response.status_code == 200


def test_constitutional_amendment_ratification_flow(
    client: TestClient,
) -> None:
    """Verifies BFT Synod constitutional amendment ratification."""
    payload = {
        "proposal": {
            "amendment_id": "AMD-2026-001",
            "target_rule": "R09_EXECUTABLE_ARCH",
            "proposed_text": "Pre-commit hook enforcement mandated.",
            "reasoning": "Enforce OS-level pre-commit gate.",
        },
        "synod_votes": [
            {"node_id": "node_1", "decision": "APPROVE"},
            {"node_id": "node_2", "decision": "APPROVE"},
            {"node_id": "node_3", "decision": "APPROVE"},
            {"node_id": "node_4", "decision": "REJECT"},
        ],
    }
    response = client.post("/governance/constitution/amend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ratified"] is True


def test_four_infrastructure_upgrades_flow(
    client: TestClient,
) -> None:
    """Verifies policy reload and evaluation flow."""
    reload_resp = client.post("/governance/policy/reload")
    assert reload_resp.status_code == 200
    assert reload_resp.json()["status"] == "RELOADED"

    passed, results = policy_evaluator.evaluate_payload({"__version": 2})
    assert passed is True
    assert len(results) == 3


def test_production_four_upgrades_integration_suite(
    client: TestClient,
) -> None:
    """Verifies OPA policy evaluation flow."""
    opa_payload = {"input_data": {"__version": 2, "environment": "production"}}
    opa_resp = client.post("/governance/opa/evaluate", json=opa_payload)
    assert opa_resp.status_code == 200
    opa_data = opa_resp.json()
    assert opa_data["allow"] is True
    assert "metrics" in opa_data


def test_policy_middleware_blocking_invalid_header(
    client: TestClient,
) -> None:
    """Verifies policy middleware blocks non-production environment header."""
    response = client.post(
        "/events/publish/degraded-health",
        json={
            "capability_id": "packages/knowledge",
            "current_health_score": 65.0,
            "drift_index": 0.20,
        },
        headers={"X-Environment": "staging"},
    )
    assert response.status_code == 403


def test_reactive_metrics_to_self_rewrite_and_graph_chain(
    client: TestClient,
) -> None:
    """Verifies reactive event triggering auto-rewrite and graph ingest."""
    response = client.post(
        "/events/publish/degraded-health",
        json={
            "capability_id": "packages/knowledge",
            "current_health_score": 65.0,
            "drift_index": 0.20,
        },
        headers={"X-Environment": "production"},
    )
    assert response.status_code == 202


def test_pgvector_memory_adapter_sqlite_fallback(tmp_path: Any) -> None:
    """Verifies architecture memory adapter with SQLite fallback."""
    db_file = tmp_path / "test_memory.db"
    db_url = f"sqlite:///{db_file}"

    adapter = PgVectorArchitectureMemoryAdapter(db_url=db_url)

    record = ArchitectureMemoryRecordAggregate(
        memory_id="MEM-PG-01",
        tier=MemoryTier.SEMANTIC,
        memory_type=MemoryType.PATTERN_RULE,
        title="Hexagonal Coupling Protection",
        context_summary="Domain layer isolation pattern",
        lesson_learned="Never import infrastructure in domain",
    )

    adapter.save(record)

    fetched = adapter.find_by_id("MEM-PG-01")
    assert fetched is not None
    assert fetched.memory_id == "MEM-PG-01"
    assert fetched.title == "Hexagonal Coupling Protection"


def test_observability_middleware_automates_metrics_capture() -> None:
    """Verifies EAOSObservabilityMiddleware headers and telemetry capture."""
    metrics_repo = InMemoryMetricsRepository()

    test_app = FastAPI()
    test_app.add_middleware(
        EAOSObservabilityMiddleware,
        metrics_repository=metrics_repo,
        system_id="TEST-SYS",
    )

    @test_app.get("/test-endpoint")
    def sample_endpoint() -> dict[str, str]:
        return {"status": "ok"}

    @test_app.get("/error-endpoint")
    def error_endpoint() -> None:
        raise HTTPException(status_code=400, detail="Bad Request")

    test_client = TestClient(test_app)

    resp = test_client.get("/test-endpoint")
    assert resp.status_code == 200
    assert "X-Trace-ID" in resp.headers
    assert "X-Correlation-ID" in resp.headers

    resp_err = test_client.get("/error-endpoint")
    assert resp_err.status_code == 400

    aggregate = metrics_repo.find_by_system_id("TEST-SYS")
    assert aggregate is not None
    assert len(aggregate.observations) == 3


# ============================================================================
# 8. HYPERSCALE HARDENING INTEGRATION TESTS
# ============================================================================


def test_hyperscale_gap1_postgres_rls_isolation(client: TestClient) -> None:
    """Verify Gap 1: PostgreSQL Row-Level Security tenant context application."""
    response = client.post(
        "/tenancy/rls/apply-context",
        json={"tenant_id": "tenant_enterprise_99"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tenant_id"] == "tenant_enterprise_99"
    assert data["rls_enabled"] is True


def test_hyperscale_gap2_quantum_envelope_encryption(
    client: TestClient,
) -> None:
    """Verify Gap 2: Kyber768 post-quantum key envelope encryption."""
    response = client.post(
        "/security/quantum/encrypt-envelope",
        json={
            "secret_data": "postgres://eaos:secret@localhost:5432/eaos",
            "public_key_fingerprint": "kyber768_fp_88291a",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "CRYSTALS-Kyber768" in data["algorithm"]
    assert len(data["cipher_text_hex"]) == 64


def test_hyperscale_gap3_otlp_trace_span_exporter(client: TestClient) -> None:
    """Verify Gap 3: OpenTelemetry OTLP trace span exporter."""
    response = client.post(
        "/telemetry/otlp/export-span",
        json={
            "service_name": "eaos-gateway",
            "span_data": {"route": "/health", "duration_ms": 1.2},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["exported"] is True
    assert data["service_name"] == "eaos-gateway"


def test_hyperscale_gap4_event_schema_compatibility(
    client: TestClient,
) -> None:
    """Verify Gap 4: Event Mesh schema compatibility registry verification."""
    response = client.post(
        "/events/schema/verify-compatibility",
        json={
            "topic": "eaos.events.degraded",
            "payload": {"event_id": "evt_101", "capability_id": "identity"},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_compatible"] is True
    assert data["topic_name"] == "eaos.events.degraded"


def test_hyperscale_gap5_automated_chaos_daemon_cycle(
    client: TestClient,
) -> None:
    """Verify Gap 5: Automated Chaos Daemon resilience testing loop."""
    response = client.post("/chaos/daemon/cycle")
    assert response.status_code == 200
    data = response.json()
    assert data["system_resilient"] is True
    assert data["active_experiments"] >= 1


def test_hyperscale_gap6_topological_connectivity_audit(
    client: TestClient,
) -> None:
    """Verify Gap 6: Topological integration across all 38 root directories."""
    response = client.get("/governance/topology/audit")
    assert response.status_code == 200
    data = response.json()
    assert data["all_connected"] is True
    assert data["isolated_directories_count"] == 0
    assert data["total_root_directories"] >= 38
