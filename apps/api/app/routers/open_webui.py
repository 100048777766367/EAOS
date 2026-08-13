"""Open WebUI OpenAI-compatible Gateway Router."""

from __future__ import annotations

import json
import uuid
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any, Final

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from apps.api.app.schemas.chat import ChatCompletionRequest
from apps.api.app.services.chat.orchestrator import ChatOrchestrator

router: Final[APIRouter] = APIRouter(tags=["Open WebUI Gateway"])

PROJECT_ROOT = Path(__file__).resolve().parents[4]
orchestrator = ChatOrchestrator(PROJECT_ROOT)


@router.get("/v1/models")
async def list_models() -> dict[str, Any]:
    """List available OpenAI-compatible models."""
    return {
        "object": "list",
        "data": [
            {
                "id": "eaos",
                "object": "model",
                "created": 1700000000,
                "owned_by": "eaos",
            },
        ],
    }


def _extract_system_instruction(
    req: ChatCompletionRequest,
) -> str:
    """Extract system messages from an OpenAI-compatible request."""
    return "\n\n".join(message.content for message in req.messages if message.role == "system").strip()


def _extract_user_message(
    req: ChatCompletionRequest,
) -> str:
    """Extract the latest user message."""
    for message in reversed(req.messages):
        if message.role == "user":
            return message.content

    return ""


async def _run_orchestrator(
    req: ChatCompletionRequest,
) -> AsyncGenerator[dict[str, Any], None]:
    """Run the shared EAOS chat orchestrator."""
    message = _extract_user_message(req)

    if not message:
        raise ValueError("At least one user message is required.")

    system_instruction = _extract_system_instruction(req)

    conversation_id = f"openwebui-{uuid.uuid4().hex}"

    async for event in orchestrator.process_goal(
        conversation_id=conversation_id,
        message=message,
        system_instruction=system_instruction,
        active_file="apps/api/app/routers/chat.py",
        temperature=req.temperature,
        max_output_tokens=req.max_output_tokens,
        json_mode=req.json_mode,
    ):
        yield event


async def _event_generator(
    req: ChatCompletionRequest,
) -> AsyncGenerator[str, None]:
    """Translate EAOS stream events to OpenAI-compatible SSE."""
    completion_id = f"chatcmpl-eaos-{uuid.uuid4().hex[:12]}"

    async for event in _run_orchestrator(req):
        event_type = event.get("type")

        if event_type == "stream_chunk":
            content = str(event.get("content", ""))

            if not content:
                continue

            chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": 1700000000,
                "model": req.model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                            "content": content,
                        },
                        "finish_reason": None,
                    }
                ],
            }

            yield (
                "data: "
                + json.dumps(
                    chunk,
                    ensure_ascii=False,
                )
                + "\n\n"
            )

        elif event_type == "stream_end":
            finish_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": 1700000000,
                "model": req.model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop",
                    }
                ],
            }

            yield (
                "data: "
                + json.dumps(
                    finish_chunk,
                    ensure_ascii=False,
                )
                + "\n\n"
            )

    yield "data: [DONE]\n\n"


@router.post(
    "/v1/chat/completions",
    response_model=None,
)
async def chat_completions(
    req: ChatCompletionRequest,
) -> StreamingResponse | dict[str, Any]:
    """OpenAI-compatible chat completions backed by EAOS."""
    if req.stream:
        return StreamingResponse(
            _event_generator(req),
            media_type="text/event-stream",
        )

    full_response = ""

    async for event in _run_orchestrator(req):
        if event.get("type") == "response_complete" or (event.get("type") == "stream_end" and not full_response):
            full_response = str(event.get("reply", ""))

    if not full_response:
        raise RuntimeError("EAOS ChatOrchestrator returned an empty response.")

    return {
        "id": f"chatcmpl-eaos-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": 1700000000,
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": full_response,
                },
                "finish_reason": "stop",
            }
        ],
    }
