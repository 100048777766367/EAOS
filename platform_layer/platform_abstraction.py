"""Platform abstraction layer unifying core enterprise capabilities."""

from pydantic import BaseModel, ConfigDict


class PlatformCapabilityStatusDTO(BaseModel):
    """Value object representing high-level platform status."""

    model_config = ConfigDict(frozen=True)

    platform_module: str
    is_active: bool
    description: str


class EnterprisePlatformRegistry:
    """High-level abstraction layer over platform infrastructure."""

    MODULES: tuple[str, ...] = (
        "identity",
        "messaging",
        "security",
        "storage",
        "monitoring",
    )

    def get_platform_status(self) -> list[PlatformCapabilityStatusDTO]:
        """Returns high-level platform abstraction health status."""
        return [
            PlatformCapabilityStatusDTO(
                platform_module=mod,
                is_active=True,
                description=f"Enterprise platform abstraction: {mod}",
            )
            for mod in self.MODULES
        ]
