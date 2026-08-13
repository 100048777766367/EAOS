"""API Gateway Router for EAOS Autonomous Engineering Loop."""

from __future__ import annotations

from typing import Any

from digitaltwin.models.canonical_graph_model import BlastRadiusCategory
from engine.master_engine import EAOSMasterEngine
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/v1/engine/loop", tags=["Autonomous Engineering Loop"])

master_engine = EAOSMasterEngine()


class EngineeringLoopRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    task_id: str
    raw_user_request: str
    target_files: list[str]
    required_authority: str = "L2"
    blast_radius: str = "LOCAL"


@router.post("/run")
async def run_autonomous_engineering_loop(payload: EngineeringLoopRequest) -> dict[str, Any]:
    """Executes the full 17-stage bounded autonomous engineering lifecycle loop."""
    if not payload.target_files:
        raise HTTPException(status_code=400, detail="target_files list must not be empty")

    try:
        radius_enum = BlastRadiusCategory[payload.blast_radius.upper()]
    except KeyError:
        radius_enum = BlastRadiusCategory.LOCAL

    result = master_engine.run_autonomous_loop(
        task_id=payload.task_id,
        raw_user_request=payload.raw_user_request,
        target_files=payload.target_files,
        required_authority=payload.required_authority,
        blast_radius=radius_enum,
    )

    return {
        "loop_id": result.loop_id,
        "task_id": result.task_id,
        "intent_summary": result.intent.interpreted_objective,
        "system_state": result.system_state.state.value,
        "strategy": result.strategy_decision.selected_strategy.value,
        "is_converged": result.is_converged,
        "is_escalated": result.is_escalated,
        "escalation_reason": result.escalation_report.reason if result.escalation_report else None,
        "evidence_token": result.evidence_token,
        "timestamp": result.timestamp,
    }


@router.get("/status/{loop_id}")
async def get_engineering_loop_status(loop_id: str) -> dict[str, Any]:
    """Retrieves engineering task memory record by loop ID."""
    rec = master_engine.memory_store.get_record(loop_id)
    if not rec:
        raise HTTPException(status_code=404, detail=f"Loop record '{loop_id}' not found")
    return rec.__dict__
