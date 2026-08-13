"""Events Schema and Chaos Engineering Router."""

from typing import Annotated, Any

from fastapi import APIRouter, Body, Header, Response, status
from kernel.events.schema_registry import EventSchemaValidationDTO
from kernel.events.stream_replay import EventStreamReplayEngine, EventStreamSnapshot
from packages.knowledge_graph.application.dto import (
    IngestGraphBatchCommand,
    NodeIngestDTO,
)
from packages.knowledge_graph.application.use_cases import IngestKnowledgeGraphUseCase
from packages.knowledge_graph.domain.models import NodeType
from packages.self_rewrite.application.dto import SelfRewriteRequest
from packages.self_rewrite.application.use_cases import RunSelfRewriteUseCase
from tools.chaos.chaos_daemon import ChaosDaemonStatusDTO
from tools.chaos.chaos_engine import ChaosEngine, ChaosExperimentResult

from apps.api.app.container import (
    chaos_daemon,
    knowledge_graph_adapter,
    schema_verifier,
    self_rewrite_repo,
)

router = APIRouter(tags=["Events & Chaos"])


@router.post("/events/schema/verify-compatibility", response_model=EventSchemaValidationDTO)
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
    return schema_verifier.verify_event_compatibility(topic=t_name or "default.topic", payload=p_data or {})


@router.post("/events/publish/degraded-health", status_code=202)
async def publish_degraded_health_event(
    payload: dict[str, Any],
    response: Response,
    x_environment: Annotated[str | None, Header(alias="X-Environment")] = None,
) -> dict[str, str]:
    if x_environment != "production":
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"detail": "Environment blocked by policy guard"}

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


@router.post("/events/stream/replay")
async def replay_event_stream(
    request: dict[str, Any] | None = None,
    start_time: Annotated[str | None, Body(embed=True)] = None,
) -> EventStreamSnapshot:
    s_time = start_time
    if not s_time and isinstance(request, dict):
        s_time = str(request.get("start_time", "2026-01-01T00:00:00Z"))
    engine = EventStreamReplayEngine()
    return engine.replay_stream(start_time=s_time or "2026-01-01T00:00:00Z")


@router.post("/chaos/daemon/cycle", response_model=ChaosDaemonStatusDTO)
async def execute_chaos_daemon_cycle() -> ChaosDaemonStatusDTO:
    return chaos_daemon.run_chaos_cycle()


@router.post("/chaos/inject-fault")
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
