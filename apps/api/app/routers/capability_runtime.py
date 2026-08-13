from fastapi import APIRouter
from packages.capability.domain.models import BusinessCapability

from apps.api.app.container import capability_registry

"""Capability Runtime Router."""


router = APIRouter(prefix="/v1/capabilities", tags=["Capability Runtime"])


@router.get("", response_model=list[BusinessCapability])
async def v1_list_capabilities() -> list[BusinessCapability]:
    return capability_registry.list_all()
