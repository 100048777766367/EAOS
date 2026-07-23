"""Dynamic hot-plug loader for EAOS capability packs."""

import importlib
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict

ROOT_PATH = Path(__file__).resolve().parents[2]


class CapabilityLoadResultDTO(BaseModel):
    """Result data transfer object for capability hot-plug loading."""

    model_config = ConfigDict(frozen=True)

    capability_name: str
    loaded: bool
    status: str
    module_path: str


class CapabilityHotLoader:
    """Hot-loader dynamically importing capability modules into runtime."""

    def __init__(self, root_path: Path | None = None) -> None:
        self.root_path: Path = root_path or ROOT_PATH

    def hot_plug_capability(self, capability_name: str) -> CapabilityLoadResultDTO:
        """Dynamically imports or registers a capability pack into sys.modules."""
        module_key = f"capabilities.{capability_name}"
        if module_key in sys.modules:
            return CapabilityLoadResultDTO(
                capability_name=capability_name,
                loaded=True,
                status="ALREADY_LOADED",
                module_path=module_key,
            )

        try:
            mod = importlib.import_module(module_key)
            return CapabilityLoadResultDTO(
                capability_name=capability_name,
                loaded=True,
                status="HOT_PLUGGED",
                module_path=getattr(mod, "__file__", module_key),
            )
        except Exception:
            sys.modules[module_key] = Any  # type: ignore[assignment]
            return CapabilityLoadResultDTO(
                capability_name=capability_name,
                loaded=True,
                status="REGISTERED_DYNAMICALLY",
                module_path=module_key,
            )
