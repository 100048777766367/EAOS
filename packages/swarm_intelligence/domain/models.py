from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Swarm Intelligence & Biomimetic Domain Models for EAOS Platform."""


class InsectRoleEnum(StrEnum):
    """Swarm roles inspired by insect ecosystem capabilities."""

    WORKER_ANT = "WORKER_ANT"
    PHEROMONE_SCOUT = "PHEROMONE_SCOUT"
    APEX_GUARD_MANTIS = "APEX_GUARD_MANTIS"
    SPIDER_WEAVER = "SPIDER_WEAVER"
    DRAGONFLY_PROBE = "DRAGONFLY_PROBE"
    METAMORPHOSIS_AGENT = "METAMORPHOSIS_AGENT"
    RESILIENT_COCKROACH = "RESILIENT_COCKROACH"
    DECOMPOSER_TERMITE = "DECOMPOSER_TERMITE"


class PheromoneSignalVO(BaseModel):
    """Value object representing stigmergic swarm communication."""

    model_config = ConfigDict(frozen=True)

    signal_id: str
    origin_role: InsectRoleEnum
    intensity: float = Field(default=1.0)
    topic_target: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class SwarmAgentProfile(BaseModel):
    """Entity representing a specialized biomimetic swarm agent."""

    model_config = ConfigDict(frozen=True)

    agent_id: str = Field(..., description="Unique Swarm Agent ID")
    role: InsectRoleEnum
    specialization: str
    status: str = Field(default="ACTIVE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
