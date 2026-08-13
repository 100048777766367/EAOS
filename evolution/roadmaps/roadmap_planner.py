from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Strategic 6-Horizons Roadmap Planner Engine."""


class HorizonDTO(BaseModel):
    """Value object representing a Strategic Horizon."""

    model_config = ConfigDict(frozen=True)

    horizon_number: int = Field(..., description="Horizon 1-6")
    title: str = Field(..., description="Horizon title")
    status: str = Field(default="ACTIVE")


class StrategicRoadmapPlanner:
    """Planner managing the 6 Strategic Horizons Roadmap."""

    def get_active_horizons(self) -> list[HorizonDTO]:
        """Return current 6 Strategic Horizons."""
        return [
            HorizonDTO(
                horizon_number=1,
                title="Architecture Knowledge API Layer",
                status="ACTIVE",
            ),
            HorizonDTO(
                horizon_number=2,
                title="Fitness Telemetry Bridge",
                status="ACTIVE",
            ),
            HorizonDTO(
                horizon_number=3,
                title="Multi-Agent Governance & OPA",
                status="ACTIVE",
            ),
            HorizonDTO(
                horizon_number=4,
                title="Distributed Federation & Consensus",
                status="ACTIVE",
            ),
            HorizonDTO(
                horizon_number=5,
                title="Post-Quantum Security & ZK Proofs",
                status="ACTIVE",
            ),
            HorizonDTO(
                horizon_number=6,
                title="Autonomous Cybernetics & WASM Sandbox",
                status="ACTIVE",
            ),
        ]
