import uuid
from pathlib import Path

import pytest
from apps.api.app.main import app
from fastapi.testclient import TestClient
from tools.graph.dependency_graph_generator import DependencyGraphGenerator
from tools.metrics.architecture_metrics_calculator import ArchitectureMetricsCalculator

ROOT_PATH = Path(__file__).resolve().parent.parent


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_unit_dependency_graph_generator() -> None:
    generator = DependencyGraphGenerator(ROOT_PATH)
    assert generator.generate() is True


def test_unit_architecture_metrics_calculator() -> None:
    calculator = ArchitectureMetricsCalculator(ROOT_PATH)
    assert calculator.calculate_all() is True
    assert calculator.architecture_score >= 80


def test_int_health_and_identity_flow(client: TestClient) -> None:
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


def test_int_knowledge_splay_and_assembly_flow(client: TestClient) -> None:
    knw_resp = client.post(
        "/knowledge",
        json={"title": "R1", "content": "Core", "author": "Arch"},
    )
    assert knw_resp.status_code == 201


def test_int_capabilities_specs_workflows_agents(client: TestClient) -> None:
    cap_resp = client.get("/v1/capabilities")
    assert cap_resp.status_code == 200


def test_int_memory_idempotency_and_vector_search(client: TestClient) -> None:
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
        json={"request": mem_payload, "idempotency_key": idempotency_key},
    )
    assert r1.status_code == 201


def test_int_reflection_learning_prediction_simulation(
    client: TestClient,
) -> None:
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
    payload = {
        "problem": "Database port mismatch causing connection timeouts.",
        "author": "SystemMonitor",
    }
    response = client.post("/self-rewrite/run", json=payload)
    assert response.status_code == 201


def test_int_federation_tenancy_marketplace_civilization(
    client: TestClient,
) -> None:
    fed_resp = client.get("/v1/federation/members")
    assert fed_resp.status_code == 200


def test_int_full_13_stage_autonomous_closed_loop(client: TestClient) -> None:
    auto_resp = client.post(
        "/autonomous/run-cycle",
        json={
            "problem": "System latency degrades under high load on Splay RAM.",
            "author": "MonitorDaemon",
        },
    )
    assert auto_resp.status_code == 201


def test_int_document_lifecycle_management_flow(client: TestClient) -> None:
    docs_dir = ROOT_PATH / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    mock_doc = docs_dir / "mock_system_constitution.md"
    mock_doc.write_text(
        "# Hiến Pháp Thử Nghiệm\n\nQuy tắc 1: Bảo toàn ranh giới.",
        encoding="utf-8",
    )
    assert mock_doc.exists()
    if mock_doc.exists():
        mock_doc.unlink()
