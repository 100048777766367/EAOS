"""Intelligence router handling FinOps routing, drift guard, and search."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from packages.intelligence.infrastructure.adapters import (
    ModelDriftGuardAdapter,
)
from packages.intelligence.infrastructure.model_router import (
    FinOpsModelRouter,
    ModelRoutingDecision,
)
from packages.memory.infrastructure.hybrid_graph_vector import (
    HybridGraphVectorRetriever,
    HybridSearchResult,
)

router = APIRouter(prefix="", tags=["Intelligence"])
drift_guard = ModelDriftGuardAdapter()
finops_router = FinOpsModelRouter()
hybrid_retriever = HybridGraphVectorRetriever()


@router.post("/intelligence/drift/evaluate")
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

    report = drift_guard.evaluate_drift(
        prompt=p_text or "",
        response=r_text or "",
        baseline=b_text or "",
    )
    return report.model_dump()


@router.post("/intelligence/models/route")
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

    return finops_router.route_task(
        prompt=p_text or "default task",
        max_budget_usd=b_usd if b_usd is not None else 0.05,
    )


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

    return hybrid_retriever.hybrid_search(query=search_query)
