"""Gateway task lifecycle API and event stream contracts."""

from typing import Any

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ConfigDict, Field

from apps.api.app.task_lifecycle import TaskStatusDTO, task_lifecycle_service

router = APIRouter(tags=["Task Lifecycle"])


class CommandExecutionRequest(BaseModel):
    """Engineering command submitted to the Gateway authority boundary."""

    model_config = ConfigDict(frozen=True, strict=True)

    command: str = Field(min_length=1, max_length=500)
    target_agent: str = Field(default="planner")


class CommandExecutionResponse(BaseModel):
    """Task creation response preserving the existing control route."""

    model_config = ConfigDict(frozen=True)

    status: str
    task_id: str
    lifecycle_state: str
    output: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


@router.post("/api/v1/control/execute", response_model=CommandExecutionResponse)
async def execute_command(payload: CommandExecutionRequest) -> CommandExecutionResponse:
    """Submit a governed task and return its real Gateway task identifier."""

    status = await task_lifecycle_service.submit(
        command=payload.command.strip(),
        target_agent=payload.target_agent,
    )
    return CommandExecutionResponse(
        status=status.lifecycle_state.value,
        task_id=status.task_id,
        lifecycle_state=status.lifecycle_state.value,
        output=status.output,
        metadata={
            "target": status.target_agent,
            "governance": status.governance,
            "verification": status.verification,
            "evidence": status.evidence,
            "error": status.error,
            "correlation_id": status.correlation_id,
        },
    )


@router.get("/api/v1/tasks/{task_id}", response_model=TaskStatusDTO)
async def get_task_status(task_id: str) -> TaskStatusDTO:
    """Return real lifecycle state for a Gateway-owned task."""

    status = task_lifecycle_service.get(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="task not found")
    return status


@router.websocket("/api/v1/tasks/{task_id}/events")
async def task_events(websocket: WebSocket, task_id: str) -> None:
    """Stream recorded lifecycle events for a Gateway-owned task."""

    await websocket.accept()
    if task_lifecycle_service.get(task_id) is None:
        await websocket.send_json({"error": {"message": "task not found"}})
        await websocket.close(code=1008)
        return
    sent = 0
    try:
        while True:
            events = task_lifecycle_service.events_for(task_id)
            for event in events[sent:]:
                await websocket.send_json(event.model_dump(mode="json"))
            sent = len(events)
            current = task_lifecycle_service.get(task_id)
            if current and current.lifecycle_state.value in {
                "completed",
                "failed",
                "denied",
            }:
                await websocket.close(code=1000)
                return
            await task_lifecycle_service.wait_for_event_count(task_id, sent)
    except WebSocketDisconnect:
        return
