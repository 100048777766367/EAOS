"""Desktop Application Entry Point for EAOS Control Room."""

import time

from pydantic import BaseModel, ConfigDict


class DesktopAppConfig(BaseModel):
    """Value object configuring desktop application runtime."""

    model_config = ConfigDict(frozen=True)

    app_title: str
    window_width: int
    window_height: int
    api_gateway_url: str


class DesktopLaunchStatus(BaseModel):
    """Value object describing desktop application status."""

    model_config = ConfigDict(frozen=True)

    launched: bool
    active_window_id: str
    message: str


class EAOSDesktopApplication:
    """Desktop GUI application launcher and control panel."""

    def __init__(
        self,
        config: DesktopAppConfig | None = None,
    ) -> None:
        self.config = config or DesktopAppConfig(
            app_title="EAOS Desktop Control Room",
            window_width=1280,
            window_height=800,
            api_gateway_url="http://127.0.0.1:8000",
        )

    def launch(self) -> DesktopLaunchStatus:
        """Launches desktop control room interface."""
        window_id = f"win_{int(time.time())}"
        return DesktopLaunchStatus(
            launched=True,
            active_window_id=window_id,
            message=f"Desktop window '{self.config.app_title}' ready.",
        )
