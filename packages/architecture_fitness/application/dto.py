"""DTOs for Architecture Fitness application layer."""

from packages.architecture_fitness.domain.models import FitnessDimension
from pydantic import BaseModel


class EvaluationItemDTO(BaseModel):
    dimension: FitnessDimension
    rule_id: str
    passed: bool
    score: float
    evidence_details: str


class EvaluateFitnessSuiteCommand(BaseModel):
    suite_id: str
    business_goal_id: str
    capability_id: str
    adr_id: str
    rule_id: str
    commit_hash: str
    author_id: str
    incident_id: str | None = None
    evaluations: list[EvaluationItemDTO]


class ADRIncidentImpactResponse(BaseModel):
    adr_id: str
    incident_count: int
    rank: int
