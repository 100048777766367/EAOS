from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""CRM and Sales Lead Domain Model for EAOS Capability App."""


class SalesLead(BaseModel):
    """Value object representing a CRM customer lead."""

    model_config = ConfigDict(frozen=True)

    lead_id: str = Field(..., description="Unique Lead ID")
    email: str = Field(..., description="Customer email address")
    source: str = Field(default="CONTENT_FUNNEL")
    score: float = Field(default=0.0)
    status: str = Field(default="NEW")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
