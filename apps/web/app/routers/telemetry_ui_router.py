import asyncio
from collections.abc import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

"""Telemetry and Live SSE Stream UI Router."""


router = APIRouter(prefix="/telemetry-ui", tags=["UI Telemetry"])


async def generate_ui_stream() -> AsyncGenerator[str]:
    """Generates live Server-Sent Events (SSE) metrics for Web UI."""
    step = 0
    while True:
        await asyncio.sleep(2)
        step += 1
        data_json = f'{{"step": {step}, "active_users": 1, "agent_tasks": 3, "system_load": 0.12}}'
        yield f"data: {data_json}\n\n"


@router.get("/stream")
async def stream_ui_telemetry() -> StreamingResponse:
    """Live SSE stream for real-time telemetry dashboard."""
    return StreamingResponse(
        generate_ui_stream(),
        media_type="text/event-stream",
    )
