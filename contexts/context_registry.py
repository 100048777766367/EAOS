from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from contexts.crm.crm_context import BoundedContextDTO, CRMContextRegistry
from contexts.sales.sales_context import SalesContextRegistry

"""Master DDD Bounded Context Registry and Context Map Engine."""


class ContextMapRelationshipDTO(BaseModel):
    """Relationship edge in DDD Context Map."""

    model_config = ConfigDict(frozen=True)

    upstream_context: str
    downstream_context: str
    pattern: str = Field(default="SHARED_KERNEL")


class EnterpriseContextMapDTO(BaseModel):
    """Aggregate Context Map for all DDD Bounded Contexts."""

    model_config = ConfigDict(frozen=True)

    total_contexts: int = Field(default=0)
    contexts: list[BoundedContextDTO] = Field(default_factory=list)
    relationships: list[ContextMapRelationshipDTO] = Field(default_factory=list)


class BoundedContextRegistryEngine:
    """Master Engine orchestrating DDD Bounded Contexts and Context Map."""

    def __init__(self) -> None:
        self.crm_reg = CRMContextRegistry()
        self.sls_reg = SalesContextRegistry()

    def generate_context_map(self) -> EnterpriseContextMapDTO:
        """Generate master enterprise DDD context map."""
        crm_dto = self.crm_reg.get_context_dto()
        sls_dto = self.sls_reg.get_context_dto()

        all_contexts = [
            crm_dto,
            sls_dto,
            BoundedContextDTO(
                context_id="finance",
                name="Financial Management & P&L",
                primary_entities=["Account", "GeneralLedger"],
            ),
            BoundedContextDTO(
                context_id="marketing",
                name="Marketing & Growth Funnels",
                primary_entities=["Campaign", "KeywordSpec"],
            ),
        ]

        relationships = [
            ContextMapRelationshipDTO(
                upstream_context="crm",
                downstream_context="sales",
                pattern="CUSTOMER_SUPPLIER",
            ),
            ContextMapRelationshipDTO(
                upstream_context="sales",
                downstream_context="finance",
                pattern="UPSTREAM_DOWNSTREAM",
            ),
        ]

        return EnterpriseContextMapDTO(
            total_contexts=len(all_contexts),
            contexts=all_contexts,
            relationships=relationships,
        )
