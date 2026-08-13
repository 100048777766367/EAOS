"""HTTP routes for the EAOS AI Studio."""

from __future__ import annotations

import os
import platform
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["AI Studio Core"])


PROJECT_ROOT = Path(__file__).resolve().parents[4]

templates = Jinja2Templates(
    directory=str(
        PROJECT_ROOT / "apps" / "api" / "app" / "templates"
    )
)


@router.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request) -> HTMLResponse:
    """Serve the EAOS AI Studio workspace."""
    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={
            "request": request,
            "title": "EAOS Enterprise AI IDE Studio",
        },
    )


@router.get("/v1/runtime/footer")
async def runtime_footer(
    request: Request,
) -> dict[str, Any]:
    """Return non-secret runtime metadata for the UI."""

    client = request.client

    return {
        "runtime": "eaos-api",
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": os.path.abspath(
            os.sys.executable # pyright: ignore[reportAttributeAccessIssue]
        ),
        "process_id": os.getpid(),
        "working_directory": os.getcwd(),
        "api_host": (
            str(request.url.hostname)
            if request.url.hostname
            else "unknown"
        ),
        "api_port": request.url.port,
        "client_host": (
            client.host
            if client is not None
            else None
        ),
        "llm_provider": os.getenv(
            "DEFAULT_AI_PROVIDER",
            "gemini",
        ).strip().lower(),
        "gemini_model": os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash",
        ).strip().removeprefix("models/"),
        "ollama_model": os.getenv(
            "OLLAMA_MODEL",
            "nemotron-mini:latest",
        ).strip(),
    }