from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from apps.web.app.presenters.control_room_presenter import ControlRoomPresenter

"""Control Room Router cho apps/web."""


router = APIRouter(prefix="", tags=["Web Control Room"])


def get_presenter() -> ControlRoomPresenter:
    return ControlRoomPresenter()


@router.get("/dashboard", response_class=HTMLResponse)
@router.get("/control-room", response_class=HTMLResponse)
async def render_control_room_dashboard(
    request: Request,
    presenter: Annotated[ControlRoomPresenter, Depends(get_presenter)],
) -> Any:
    """Render giao diện Dashboard UI sạch sẽ qua Jinja2."""
    return presenter.render_dashboard(request)
