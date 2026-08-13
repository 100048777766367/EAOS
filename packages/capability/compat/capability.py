import uuid

from pydantic import BaseModel, ConfigDict, Field

"""Non-destructive compatibility layer for legacy capability contracts."""


class BusinessCapability(BaseModel):
    """Legacy Business Capability contract restored for backward compatibility."""

    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: f"cap_{uuid.uuid4().hex[:8]}")
    name: str
    description: str = ""
    status: str = "active"
    version: str = "1.0.0"


class CapabilityContract(BaseModel):
    """Legacy Capability Contract model."""

    model_config = ConfigDict(frozen=True)

    contract_id: str
    capability_id: str
    schema_version: str = "1.0.0"
