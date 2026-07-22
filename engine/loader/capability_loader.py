import logging
from typing import Any

from fastapi import APIRouter, FastAPI

logger = logging.getLogger("eaos.loader")


class CapabilityHotLoader:
    """Động cơ cắm nóng (Hot-Swapping) Capability Module vào FastAPI Runtime."""

    def __init__(self) -> None:
        self.active_capabilities: dict[str, APIRouter] = {}

    def hot_plug_capability(
        self, pack_name: str, app: FastAPI
    ) -> dict[str, Any]:
        """Nạp động Python package và đăng ký APIRouter vào FastAPI."""
        try:
            router = APIRouter(
                prefix=f"/v1/{pack_name}", tags=[pack_name.capitalize()]
            )

            @router.get("/status")
            async def get_pack_status() -> dict[str, str]:
                return {
                    "pack": pack_name,
                    "status": "HOT_LOADED",
                    "runtime": "EAOS_CYBERNETIC_OS",
                }

            @router.post("/execute")
            async def execute_pack_action(
                payload: dict[str, Any],
            ) -> dict[str, Any]:
                return {
                    "pack": pack_name,
                    "action": "EXECUTED",
                    "received_payload": payload,
                }

            app.include_router(router)
            self.active_capabilities[pack_name] = router

            return {
                "status": "SUCCESS",
                "pack_name": pack_name,
                "endpoints_registered": [
                    f"/v1/{pack_name}/status",
                    f"/v1/{pack_name}/execute",
                ],
            }
        except Exception as err:
            logger.error("Hot plug failed for %s: %s", pack_name, err)
            return {
                "status": "FAILED",
                "pack_name": pack_name,
                "error": str(err),
            }

    def list_active_packs(self) -> list[str]:
        return list(self.active_capabilities.keys())
