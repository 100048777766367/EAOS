"""Web Application & Control Room Dashboard Server for EAOS."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class WebDashboardConfig(BaseModel):
    """Value object configuring web dashboard server settings."""

    model_config = ConfigDict(frozen=True)

    host: str
    port: int
    dashboard_root: str


class EAOSWebControlRoomApp:
    """Web application server hosting Control Room dashboard."""

    def __init__(
        self,
        config: WebDashboardConfig | None = None,
    ) -> None:
        self.config = config or WebDashboardConfig(
            host="0.0.0.0",
            port=8000,
            dashboard_root="/dashboard",
        )

    def render_dashboard_html(self, root_path: Path) -> str:
        """Delegates rendering to ControlRoomDashboard."""
        from tools.dashboard.control_room import ControlRoomDashboard

        dashboard = ControlRoomDashboard(root_path)
        return dashboard.render_html()
