import json

from pydantic import BaseModel, ConfigDict

"""Static Asset and PWA Manifest Manager."""


class PWAManifestDTO(BaseModel):
    """Progressive Web App Manifest DTO."""

    model_config = ConfigDict(frozen=True)

    name: str = "EAOS Enterprise Operating System"
    short_name: str = "EAOS"
    theme_color: str = "#06b6d4"
    background_color: str = "#0f172a"
    display: str = "standalone"
    start_url: str = "/control-room"


class ManifestEngine:
    """Generates PWA manifests and static asset tags."""

    def __init__(self, manifest_data: PWAManifestDTO | None = None) -> None:
        self.manifest = manifest_data or PWAManifestDTO()

    def to_json(self) -> str:
        """Serializes PWA manifest DTO to formatted JSON string."""
        return json.dumps(self.manifest.model_dump(), indent=2)
