from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from apps.web.app.settings import web_settings

"""Web UI Health and Telemetry Router."""


router = APIRouter(prefix="/health", tags=["Health & Status"])


class WebHealthDTO(BaseModel):
    """Health status response model for Web Gateway."""

    model_config = ConfigDict(frozen=True)

    status: str
    channel: str
    version: str
    api_gateway: str


@router.get("", response_model=WebHealthDTO)
async def get_web_health() -> WebHealthDTO:
    """Web Gateway primary health probe."""
    return WebHealthDTO(
        status="healthy",
        channel="eaos-web-app",
        version=web_settings.version,
        api_gateway=web_settings.api_gateway_url,
    )


@router.get("/detailed")
async def get_detailed_web_health() -> dict[str, Any]:
    """Detailed status probe of Web Gateway configuration and dependencies."""
    return {
        "status": "HEALTHY",
        "channel": "eaos-web-app",
        "settings": web_settings.model_dump(exclude={"secret_key"}),
        "uptime_status": "OPERATIONAL",
    }
