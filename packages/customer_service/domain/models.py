from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Customer Service and Support Domain Model for EAOS."""


class SupportTicket(BaseModel):
    """Value object representing a customer support request ticket."""

    model_config = ConfigDict(frozen=True)

    ticket_id: str = Field(..., description="Unique Ticket ID")
    customer_id: str = Field(..., description="Customer identifier")
    issue_summary: str = Field(..., description="Problem description")
    priority: str = Field(default="HIGH")
    status: str = Field(default="OPEN")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
