from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]
from fastapi import APIRouter, FastAPI


class CapabilityHotLoader:
    """Động cơ quét và cắm nóng (Hot-Plug) Capability Packs mới vào RAM."""

    def __init__(self, app: FastAPI, capabilities_dir: Path) -> None:
        self.app = app
        self.capabilities_dir = capabilities_dir
        self.loaded_capabilities: set[str] = set()

    def scan_and_hot_plug(self) -> list[str]:
        """Tự động phát hiện capability.yaml và nạp Router động vào FastAPI."""
        newly_loaded: list[str] = []
        if not self.capabilities_dir.exists():
            return newly_loaded

        for yaml_file in self.capabilities_dir.glob("*.yaml"):
            cap_name = yaml_file.stem
            if cap_name not in self.loaded_capabilities:
                with open(yaml_file, encoding="utf-8") as f:
                    spec_data = yaml.safe_load(f) or {}

                router = APIRouter(prefix=f"/v1/{cap_name}", tags=[cap_name.upper()])

                @router.get("/spec")
                async def get_capability_spec(
                    name: str = cap_name,
                    data: dict[str, Any] = spec_data,
                ) -> dict[str, Any]:
                    return {"capability": name, "spec": data}

                self.app.include_router(router)
                self.loaded_capabilities.add(cap_name)
                newly_loaded.append(cap_name)

        return newly_loaded
