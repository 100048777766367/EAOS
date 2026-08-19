"""Health and System Status Router."""

from typing import Any

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from tools.dashboard.control_room import ControlRoomDashboard

from apps.api.app.container import ROOT_PATH
from apps.api.app.dto.api_response_dto import HealthResponse

router = APIRouter(tags=["Health & Status"])

_HEALTH_RESPONSE_CACHE = HealthResponse(
    status="healthy",
    version="0.1.0",
    governance="ARCHITECTURE_CONSTITUTION.md v2.0",
    doctor_score=100,
)


@router.get("/")
async def root_system_status() -> dict[str, Any]:
    """Root status probe providing system overview and control room links."""
    return {
        "system": "Enterprise Architecture Operating System (EAOS)",
        "status": "READY",
        "version": "0.1.0",
        "governance": "ARCHITECTURE_CONSTITUTION.md v3.0",
        "control_room_dashboard": "/dashboard",
        "api_documentation": "/docs",
        "health_check": "/health",
    }


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return _HEALTH_RESPONSE_CACHE


@router.get("/dashboard", response_class=HTMLResponse)
@router.get("/agent-control", response_class=HTMLResponse)
async def get_dashboard() -> HTMLResponse:
    dashboard = ControlRoomDashboard(ROOT_PATH)
    return HTMLResponse(content=dashboard.render_html())
