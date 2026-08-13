from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""CQRS Queries Catalog (CQRS Pattern)."""


class QueryElementDTO(BaseModel):
    """Value object representing a CQRS Query in Enterprise Catalog."""

    model_config = ConfigDict(frozen=True)

    query_id: str = Field(..., description="Query ID")
    name: str = Field(..., description="Query name e.g. GetHealthScore")
    return_type: str = Field(default="DTO")


class QueryCatalogRegistry:
    """Registry cataloging CQRS queries."""

    def get_default_queries(self) -> list[QueryElementDTO]:
        """Return standard CQRS queries."""
        return [
            QueryElementDTO(
                query_id="qry-get-health",
                name="GetSystemHealthQuery",
                return_type="DiagnosticReportDTO",
            ),
        ]
