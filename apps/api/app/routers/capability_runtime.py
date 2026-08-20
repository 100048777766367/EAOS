"""Capability Runtime Router."""

from fastapi import APIRouter

from apps.api.app.capability_contracts import GatewayCapabilityContract, list_capability_contracts

router = APIRouter(prefix="/v1/capabilities", tags=["Capability Runtime"])


@router.get("", response_model=list[GatewayCapabilityContract])
async def v1_list_capabilities() -> list[GatewayCapabilityContract]:
    """Return explicit Gateway capability contracts and documented contract gaps."""

    return list_capability_contracts()
