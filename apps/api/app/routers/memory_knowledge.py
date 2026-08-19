"""Memory and Hybrid Search Router."""

from typing import Annotated, Any, cast

from fastapi import APIRouter, Body
from packages.memory.application.dto import MemoryResponse, StoreMemoryCommand
from packages.memory.application.handlers import StoreMemoryHandler
from packages.memory.domain.entities import MemoryRecord
from packages.memory.infrastructure.hybrid_graph_vector import HybridSearchResult

from apps.api.app.container import idempotency_service, knowledge_graph_adapter, memory_repo

router = APIRouter(tags=["Memory & Search"])


@router.get("/v1/memory", response_model=list[MemoryRecord])
async def v1_list_memories() -> list[MemoryRecord]:
    return memory_repo.list_all()


@router.post("/v1/memory/store", response_model=MemoryResponse, status_code=201)
async def v1_store_memory(body: dict[str, Any]) -> MemoryResponse:
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


@router.post("/memory/hybrid-search")
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
