from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""CRM Bounded Context Definition (DDD Pattern)."""


class BoundedContextDTO(BaseModel):
    """Value object representing a DDD Bounded Context."""

    model_config = ConfigDict(frozen=True)

    context_id: str = Field(..., description="Unique Context ID e.g. crm")
    name: str = Field(..., description="Context name")
    primary_entities: list[str] = Field(default_factory=list)
    relationship: str = Field(default="SHARED_KERNEL")


class CRMContextRegistry:
    """Registry providing CRM bounded context definition."""

    def get_context_dto(self) -> BoundedContextDTO:
        """Return CRM bounded context specification."""
        return BoundedContextDTO(
            context_id="crm",
            name="Customer Relationship Management",
            primary_entities=["Customer", "Lead", "Interaction"],
            relationship="CUSTOMER_SUPPLIER",
        )
