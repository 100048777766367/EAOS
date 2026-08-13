"""API Gateway Router for EAOS Agent Capability Registry & Multi-Agent Orchestration."""

from __future__ import annotations

from typing import Any

from agents.agent_manager import AgentManager
from digitaltwin.models.canonical_graph_model import BlastRadiusCategory
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/v1/agents", tags=["Agent Capability & Orchestration"])

agent_manager = AgentManager()


class AgentSelectionRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    task_id: str
    intent: str
    task_type: str = "patch"
    required_authority: str = "L2"
    blast_radius: str = "LOCAL"


class WorkflowOrchestrationRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    task_id: str
    intent: str
    task_type: str = "patch"
    required_authority: str = "L2"
    target_files: list[str]
    blast_radius: str = "LOCAL"


@router.get("/registry")
async def get_agent_capability_registry() -> dict[str, Any]:
    """Returns all registered agent capabilities and specialized agent profiles."""
    caps = agent_manager.registry.list_all_capabilities()
    agents = agent_manager.registry.list_all_agents()
    return {
        "capabilities_count": len(caps),
        "agents_count": len(agents),
        "capabilities": [c.__dict__ for c in caps],
        "agents": [a.__dict__ for a in agents],
    }


@router.post("/select")
async def select_agents_for_task(payload: AgentSelectionRequest) -> dict[str, Any]:
    """Matches task intent & blast radius against capability registry to select implementer & verifier agents."""
    try:
        radius_enum = BlastRadiusCategory[payload.blast_radius.upper()]
    except KeyError:
        radius_enum = BlastRadiusCategory.LOCAL

    decision = agent_manager.select_agents_for_capability(
        task_id=payload.task_id,
        intent=payload.intent,
        task_type=payload.task_type,
        required_authority=payload.required_authority,
        blast_radius=radius_enum,
    )
    return {
        "task_id": decision.task_id,
        "intent": decision.intent,
        "required_authority": decision.required_authority,
        "blast_radius": decision.blast_radius.value,
        "matched_capability_ids": decision.matched_capability_ids,
        "primary_implementer_agent": (
            decision.primary_implementer_agent.__dict__ if decision.primary_implementer_agent else None
        ),
        "independent_verifier_agent": (
            decision.independent_verifier_agent.__dict__ if decision.independent_verifier_agent else None
        ),
        "requires_independent_verification": decision.requires_independent_verification,
        "is_blocked_by_governance": decision.is_blocked_by_governance,
        "blocking_reason": decision.blocking_reason,
        "timestamp": decision.timestamp,
    }


@router.post("/orchestrate")
async def orchestrate_multi_agent_workflow(
    payload: WorkflowOrchestrationRequest,
) -> dict[str, Any]:
    """Executes multi-agent pipeline with resource locking and handoff contracts."""
    if not payload.target_files:
        raise HTTPException(status_code=400, detail="target_files list must not be empty")

    try:
        radius_enum = BlastRadiusCategory[payload.blast_radius.upper()]
    except KeyError:
        radius_enum = BlastRadiusCategory.LOCAL

    wf_result = agent_manager.execute_multi_agent_workflow(
        task_id=payload.task_id,
        intent=payload.intent,
        task_type=payload.task_type,
        required_authority=payload.required_authority,
        target_files=payload.target_files,
        blast_radius=radius_enum,
    )
    return {
        "workflow_id": wf_result.workflow_id,
        "task_id": wf_result.task_id,
        "overall_success": wf_result.overall_success,
        "is_blocked_by_governance": (wf_result.selection_decision.is_blocked_by_governance),
        "blocking_reason": wf_result.selection_decision.blocking_reason,
        "steps_executed": len(wf_result.steps),
        "steps": [s.__dict__ for s in wf_result.steps],
        "locks_held": wf_result.locks_held,
        "evidence_token": wf_result.evidence_token,
        "timestamp": wf_result.timestamp,
    }


@router.get("/locks")
async def list_active_resource_locks() -> list[dict[str, Any]]:
    """Returns all active resource locks."""
    locks = agent_manager.lock_manager.list_active_locks()
    return [lock_item.__dict__ for lock_item in locks]
