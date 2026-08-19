"""Workspace routes for the AIDE application."""

from typing import Annotated

from apps.aide.app.adapters.gateway_probe import probe_gateway
from apps.aide.app.dependencies.settings import aide_settings
from apps.aide.app.presenters.workspace_presenter import build_domain_surface
from apps.aide.app.services.integration import (
    build_gateway_snapshot,
    list_gateway_contracts,
    submit_task,
)
from apps.aide.app.services.workspace import build_workspace_state
from apps.aide.app.settings import AideSettings
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["AIDE Workspace"])
templates = Jinja2Templates(directory="apps/aide/templates")


@router.get("/", response_class=HTMLResponse)
async def workspace(
    request: Request,
    settings: Annotated[AideSettings, Depends(aide_settings)],
) -> HTMLResponse:
    """Render the AIDE engineering workspace shell."""

    state = build_workspace_state(settings)
    return templates.TemplateResponse(
        request=request,
        name="workspace.html",
        context={"domains": build_domain_surface(), "state": state},
    )


@router.get("/workspace/state")
async def workspace_state(
    settings: Annotated[AideSettings, Depends(aide_settings)],
) -> dict[str, object]:
    """Expose browser bootstrap state for contract validation."""

    return build_workspace_state(settings).model_dump()


@router.get("/integrations/gateway/health")
async def gateway_health(
    settings: Annotated[AideSettings, Depends(aide_settings)],
) -> dict[str, str]:
    """Report observed Gateway availability for the AIDE UI."""

    return (await probe_gateway(settings)).model_dump()


@router.get("/integrations/gateway/contracts")
async def gateway_contracts() -> list[dict[str, str]]:
    """List real and missing Gateway contracts discovered for AIDE."""

    return [contract.model_dump() for contract in list_gateway_contracts()]


@router.get("/integrations/gateway/snapshot")
async def gateway_snapshot(
    settings: Annotated[AideSettings, Depends(aide_settings)],
) -> list[dict[str, object]]:
    """Observe real Gateway contracts and preserve missing capability gaps."""

    return [result.model_dump() for result in await build_gateway_snapshot(settings)]


@router.post("/interactions/tasks")
async def task_submission(
    payload: dict[str, str],
    settings: Annotated[AideSettings, Depends(aide_settings)],
) -> dict[str, object]:
    """Submit an AIDE task interaction through the existing Gateway route."""

    command = payload.get("command", "")
    target_agent = payload.get("target_agent", "planner")
    if not command.strip():
        return {
            "contract": "task-submission",
            "target": "/api/v1/control/execute",
            "status": "degraded",
            "detail": "command is required",
            "payload": {},
        }
    result = await submit_task(settings, command, target_agent)
    return result.model_dump()
