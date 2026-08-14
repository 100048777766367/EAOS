"""EAOS AI Studio WebSocket router."""

from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from runtime.state.task_lifecycle import TaskState

from apps.api.app.routers.runtime_control_router import control_plane
from apps.api.app.services.chat.orchestrator import ChatOrchestrator

router = APIRouter(tags=["AI Studio WebSocket"])

PROJECT_ROOT = __import__("pathlib").Path(__file__).resolve().parents[4]
orchestrator = ChatOrchestrator(PROJECT_ROOT)


async def _safe_send(
    websocket: WebSocket,
    payload: dict[str, Any],
) -> bool:
    try:
        await websocket.send_json(payload)
    except (WebSocketDisconnect, RuntimeError):
        return False

    return True


def _lifecycle_payload(
    state: TaskState,
    ctx: Any,
) -> dict[str, Any]:
    return {
        "type": "task_lifecycle",
        "state": state.value,
        "correlation": ctx.__dict__,
        "proof_hash": ctx.generate_proof_hash(),
    }


@router.websocket("/ws/chat")
async def websocket_chat_endpoint(
    websocket: WebSocket,
) -> None:
    """Handle EAOS AI Studio chat over WebSocket."""
    await websocket.accept()

    try:
        while True:
            raw = await websocket.receive_text()

            try:
                data: dict[str, Any] = json.loads(raw)
            except json.JSONDecodeError:
                await _safe_send(
                    websocket,
                    {
                        "type": "error",
                        "error": "Invalid JSON request.",
                    },
                )
                continue

            conversation_id = str(data.get("conversation_id", "conv-001"))
            agent_role = str(data.get("agent_role", "agent-coder"))

            fsm, ctx = control_plane.create_task(
                user_request_id=conversation_id,
                agent_id=agent_role,
            )

            fsm.transition_to(
                TaskState.QUEUED,
                f"TOKEN-QUEUE-{ctx.task_id}",
            )

            if not await _safe_send(
                websocket,
                _lifecycle_payload(TaskState.QUEUED, ctx),
            ):
                return

            fsm.transition_to(
                TaskState.RUNNING,
                f"TOKEN-RUN-{ctx.task_id}",
            )

            if not await _safe_send(
                websocket,
                _lifecycle_payload(TaskState.RUNNING, ctx),
            ):
                return

            try:
                async for event in orchestrator.process_goal(
                    conversation_id=conversation_id,
                    message=str(data.get("message", "")),
                    system_instruction=str(data.get("system_instruction", "")),
                    active_file=str(
                        data.get(
                            "active_file",
                            "apps/api/app/routers/chat.py",
                        )
                    ),
                    temperature=float(data.get("temperature", 0.7)),
                    max_output_tokens=int(data.get("max_output_tokens", 4096)),
                    json_mode=bool(data.get("json_mode", False)),
                ):
                    event["task_id"] = ctx.task_id
                    event["proof_hash"] = ctx.generate_proof_hash()

                    if not await _safe_send(
                        websocket,
                        event,
                    ):
                        return

                fsm.transition_to(
                    TaskState.VERIFYING,
                    f"TOKEN-VERIFY-{ctx.task_id}",
                )

                if not await _safe_send(
                    websocket,
                    _lifecycle_payload(
                        TaskState.VERIFYING,
                        ctx,
                    ),
                ):
                    return

                fsm.transition_to(
                    TaskState.COMPLETED,
                    f"TOKEN-COMPLETE-{ctx.task_id}",
                )

                if not await _safe_send(
                    websocket,
                    _lifecycle_payload(
                        TaskState.COMPLETED,
                        ctx,
                    ),
                ):
                    return

            except WebSocketDisconnect:
                return

            except Exception as exc:
                failure, outcome = control_plane.handle_runtime_failure(
                    ctx.task_id,
                    exc,
                    "chat_orchestrator",
                )

                await _safe_send(
                    websocket,
                    {
                        "type": "task_lifecycle",
                        "state": fsm.current_state.value,
                        "correlation": ctx.__dict__,
                        "proof_hash": ctx.generate_proof_hash(),
                        "failure": failure.__dict__,
                        "recovery_outcome": outcome.__dict__,
                    },
                )

    except WebSocketDisconnect:
        return

    except RuntimeError:
        return
