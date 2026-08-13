from typing import Any

from fastapi import APIRouter
from packages.crm.application.use_cases import IngestLeadUseCase
from pydantic import BaseModel, ConfigDict

"""FastAPI Router for CRM Capability Application."""


router = APIRouter(prefix="/v1/crm", tags=["CRM Capability"])


class LeadIngestRequest(BaseModel):
    """Value object representing lead capture payload."""

    model_config = ConfigDict(frozen=True)

    email: str
    source: str = "CONTENT_FUNNEL"


@router.post("/leads/ingest")
async def ingest_lead(request: LeadIngestRequest) -> dict[str, Any]:
    """Ingests new customer lead into CRM."""
    use_case = IngestLeadUseCase()
    lead = use_case.execute(request.email, request.source)
    return lead.model_dump()
