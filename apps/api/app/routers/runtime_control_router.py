"""EAOS Runtime Control Plane API router."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from runtime.runtime_control_plane import RuntimeControlPlane

router = APIRouter(
    prefix="/v1/runtime/control",
    tags=["Runtime Control Plane"],
)

control_plane = RuntimeControlPlane()


@router.get("/status")
async def get_runtime_control_status() -> dict[str, Any]:
    """Return runtime operational status."""
    current = control_plane.get_control_status()

    return {
        "system_health": current.system_health,
        "active_tasks_count": current.active_tasks_count,
        "last_observation": current.last_observation,
        "processes": [process.__dict__ for process in current.processes],
        "graph_nodes": [node.__dict__ for node in current.graph_nodes],
    }


@router.get("/processes")
async def list_runtime_processes() -> list[dict[str, Any]]:
    """Return active runtime processes."""
    processes = control_plane.process_manager.inspect_all_processes()

    return [process.__dict__ for process in processes]


@router.get("/tasks/{task_id}")
async def get_task_lifecycle_status(
    task_id: str,
) -> dict[str, Any]:
    """Return lifecycle information for a task."""
    fsm = control_plane.get_task_fsm(task_id)
    context = control_plane.correlation.get_context(task_id)

    if fsm is None and context is None:
        raise HTTPException(
            status_code=404,
            detail=(f"Task ID '{task_id}' not found in Runtime Control Plane"),
        )

    return {
        "task_id": task_id,
        "current_state": (fsm.current_state.value if fsm is not None else "UNKNOWN"),
        "history": ([item.__dict__ for item in fsm.history] if fsm is not None else []),
        "correlation": (context.__dict__ if context is not None else None),
        "proof_hash": (context.generate_proof_hash() if context is not None else None),
    }


@router.post("/recover/{task_id}")
async def trigger_task_bounded_recovery(
    task_id: str,
    component: str = "runtime",
) -> dict[str, Any]:
    """Trigger bounded runtime recovery."""
    fsm = control_plane.get_task_fsm(task_id)

    if fsm is None:
        fsm, _ = control_plane.create_task()

    failure, outcome = control_plane.handle_runtime_failure(
        task_id=task_id,
        exc="Triggered via API control plane recovery",
        affected_component=component,
    )

    return {
        "task_id": task_id,
        "failure_classified": failure.__dict__,
        "recovery_outcome": outcome.__dict__,
    }
