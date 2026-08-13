import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

"""Evidence-Based Public Contract Baseline for Capability Domain."""


class CapabilityContract(BaseModel):
    """Restored Capability Contract model matching existing callers."""

    model_config = ConfigDict(frozen=True)

    id: str = Field(
        default_factory=lambda: f"ctr_{uuid.uuid4().hex[:8]}",
        description="Contract ID",
    )
    type: str = Field(default="REST", description="Contract type")
    definition_path: str = Field(default="", description="Path to API spec")
    contract_id: str = Field(default="", description="Alias contract ID")
    capability_id: str = Field(default="", description="Target capability ID")
    schema_version: str = Field(default="1.0.0")


class CapabilityMetadata(BaseModel):
    """Restored Capability Metadata model matching existing callers."""

    model_config = ConfigDict(frozen=True)

    capability_id: str = Field(default="", description="Capability ID")
    name: str = Field(default="", description="Display name")
    description: str = Field(default="", description="Description")
    version: str = Field(default="1.0.0", description="Version")
    owner: str = Field(default="system", description="Owner role/agent")
    status: str = Field(default="active", description="Status")
    supported_actions: tuple[str, ...] = Field(default_factory=tuple)
    metadata: dict[str, Any] = Field(default_factory=dict)
    contracts: tuple[CapabilityContract, ...] = Field(default_factory=tuple)
    events: tuple[str, ...] = Field(default_factory=tuple)
    dependencies: tuple[str, ...] = Field(default_factory=tuple)


class BusinessCapability(BaseModel):
    """Restored Business Capability model matching existing callers."""

    model_config = ConfigDict(frozen=True)

    id: str = Field(
        default_factory=lambda: f"cap_{uuid.uuid4().hex[:8]}",
        description="Unique Capability ID",
    )
    name: str = Field(..., description="Capability Display Name")
    description: str = Field(default="", description="Capability details")
    status: str = Field(default="active", description="Capability status")
    version: str = Field(default="1.0.0", description="Capability version")
    owner: str = Field(default="system", description="Owner role")
    capability_type: str = Field(default="core", description="Domain type")

    @property
    def slug(self) -> str:
        """Property alias for legacy slug queries."""
        return self.id.lower()

    @property
    def display_name(self) -> str:
        """Property alias for display name queries."""
        return self.name


class DomainEvent(BaseModel):
    """Value object representing an immutable Enterprise Domain Event."""

    model_config = ConfigDict(frozen=True)

    event_id: str = Field(
        default_factory=lambda: f"evt_{uuid.uuid4().hex[:12]}",
        description="Unique Event UUID",
    )
    event_type: str = Field(..., description="Event Type Code")
    aggregate_id: str = Field(default="system_aggregate", description="Aggregate Identifier")
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    version: int = Field(default=1)
    causation_id: str = Field(default="")
    correlation_id: str = Field(default="")
    payload: dict[str, Any] = Field(default_factory=dict)

    def __getitem__(self, item: str) -> Any:
        """Subscriptable support for legacy dict-like callers."""
        try:
            return getattr(self, item)
        except AttributeError as e:
            raise KeyError(item) from e


class EnterpriseCapabilityContext(BaseModel):
    """Rich Enterprise Business Context injected into execution."""

    model_config = ConfigDict(frozen=True)

    tenant_id: str = Field(default="default_tenant")
    organization_id: str = Field(default="org_global")
    business_unit: str = Field(default="bu_operations")
    identity_id: str = Field(default="system_agent")
    trace_id: str = Field(default_factory=lambda: f"trc_{uuid.uuid4().hex[:12]}")
    audit_id: str = Field(default_factory=lambda: f"aud_{uuid.uuid4().hex[:12]}")
    correlation_id: str = Field(default_factory=lambda: f"cor_{uuid.uuid4().hex[:12]}")
    workflow_id: str = Field(default="")
    saga_id: str = Field(default="")
    environment: str = Field(default="production")


# Public Aliases
CapabilityContext = EnterpriseCapabilityContext


class EnterpriseCommandDTO(BaseModel):
    """Value object representing a command passed through Command Bus."""

    model_config = ConfigDict(frozen=True)

    capability_id: str
    action: str
    payload: dict[str, Any] = Field(default_factory=dict)
    context: EnterpriseCapabilityContext = Field(default_factory=lambda: EnterpriseCapabilityContext())


# Public Aliases
CapabilityExecutionCommandDTO = EnterpriseCommandDTO


class CapabilityExecutionResultDTO(BaseModel):
    """Value object representing full enterprise execution result."""

    model_config = ConfigDict(frozen=True)

    capability_id: str
    action: str
    status: str
    trace_id: str = Field(default="")
    audit_id: str = Field(default="")
    correlation_id: str = Field(default="")
    payload: dict[str, Any] = Field(default_factory=dict)
    events_emitted: tuple[DomainEvent, ...] = Field(default_factory=tuple)
    execution_time_ms: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
