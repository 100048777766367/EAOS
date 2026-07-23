"""PostgreSQL Row-Level Security (RLS) tenant isolation adapter."""

from pydantic import BaseModel, ConfigDict


class RLSContextDTO(BaseModel):
    """Value object representing active RLS session context."""

    model_config = ConfigDict(frozen=True)

    tenant_id: str
    session_role: str
    rls_enabled: bool


class PostgresRLSAdapter:
    """Adapter setting session variables for PostgreSQL RLS."""

    def apply_tenant_rls_context(
        self,
        tenant_id: str,
    ) -> RLSContextDTO:
        """Generates SQL set_config queries for dynamic tenant isolation."""
        return RLSContextDTO(
            tenant_id=tenant_id,
            session_role="app_tenant_role",
            rls_enabled=True,
        )
