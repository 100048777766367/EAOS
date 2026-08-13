from pathlib import Path
from typing import Any

from fastapi import Request
from fastapi.templating import Jinja2Templates

"""Presenter rendering Jinja2 HTML Templates cho apps/web/app."""


TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


class ControlRoomPresenter:
    """Presenter chịu trách nhiệm render giao diện Dashboard UI."""

    def render_dashboard(self, request: Request) -> Any:
        """Render trang HTML Control Room Dashboard."""
        return templates.TemplateResponse(
            request=request,
            name="control_room.html",
            context={
                "title": "EAOS Cybernetic Control Room",
                "status": "ACTIVE",
                "constitution_version": "v3.0",
                "maturity_level": "Level 5 — Evolutionary Architecture",
            },
        )

    def get_dashboard_data(self) -> dict[str, Any]:
        """Trả về dữ liệu JSON mô phỏng cho Dashboard UI."""
        return {
            "system": "EAOS Web Control Room",
            "health_score": 100,
            "active_agents": 2,
            "maturity_level": "Level 5 — Evolutionary Architecture",
        }
