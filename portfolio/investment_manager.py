"""Portfolio manager tracking initiatives, programs, and investment goals."""

from pydantic import BaseModel, ConfigDict


class InitiativeDTO(BaseModel):
    """Value object representing an enterprise portfolio initiative."""

    model_config = ConfigDict(frozen=True)

    initiative_id: str
    title: str
    budget_usd: float
    status: str


class PortfolioManagerEngine:
    """Engine governing initiatives, programs, and strategic investments."""

    def list_initiatives(self) -> list[InitiativeDTO]:
        """Lists active enterprise transformation initiatives."""
        return [
            InitiativeDTO(
                initiative_id="INIT-2026-01",
                title="EAOS Cybernetic Autonomous Evolution",
                budget_usd=150000.0,
                status="IN_PROGRESS",
            ),
            InitiativeDTO(
                initiative_id="INIT-2026-02",
                title="Post-Quantum ZK Attestation Integration",
                budget_usd=200000.0,
                status="APPROVED",
            ),
        ]
