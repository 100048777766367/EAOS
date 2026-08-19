"""Intelligence and Model Drift Router."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from packages.intelligence.infrastructure.adapters import ModelDriftGuardAdapter
from packages.intelligence.infrastructure.model_router import FinOpsModelRouter, ModelRoutingDecision

router = APIRouter(prefix="/intelligence", tags=["Intelligence"])


@router.post("/drift/evaluate")
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

    guard = ModelDriftGuardAdapter()
    report = guard.evaluate_drift(prompt=p_text or "", response=r_text or "", baseline=b_text or "")
    return report.model_dump()


@router.post("/models/route")
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
