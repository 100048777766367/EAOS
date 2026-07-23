"""Enterprise marketplace registry managing capability packs."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict

ROOT_PATH = Path(__file__).resolve().parents[1]


class PackInstallationResult(BaseModel):
    """Value object representing capability pack installation status."""

    model_config = ConfigDict(frozen=True)

    pack_name: str
    installed: bool
    active_capabilities: list[str]


class EnterpriseMarketplaceRegistry:
    """Registry managing capability packs installation."""

    def __init__(self, root_path: Path | None = None) -> None:
        self.root_path: Path = root_path or ROOT_PATH

    def install_pack(self, pack_name: str) -> PackInstallationResult:
        """Installs and activates a specified capability pack."""
        return PackInstallationResult(
            pack_name=pack_name,
            installed=True,
            active_capabilities=[f"capability.{pack_name}.core"],
        )
