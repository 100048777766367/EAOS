from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Service Delivery & SLA Domain Model for EAOS Capability App."""


class ServiceEngagement(BaseModel):
    """Value object representing a client service delivery engagement."""

    model_config = ConfigDict(frozen=True)

    engagement_id: str = Field(..., description="Unique Engagement UUID")
    client_id: str = Field(..., description="Client identifier")
    service_tier: str = Field(default="ENTERPRISE")
    sla_status: str = Field(default="COMPLIANT")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
