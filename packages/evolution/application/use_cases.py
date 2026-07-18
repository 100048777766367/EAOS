from typing import Any

from pydantic import BaseModel

from packages.evolution.domain.models import (
    Evidence,
    EvolutionObject,
    Metadata,
    Provenance,
)
from packages.evolution.domain.ports import EvolutionRepository


class ProposeEvolutionRequest(BaseModel):
    id: str
    name: str
    payload: dict[str, Any]
    author: str
    triggered_by: str
    parent_id: str | None = None
    environment: str = "production"
    criticality: str = "high"


class ProposeEvolutionUseCase:
    """Application Service điều phối việc đề xuất và lưu trữ tiến hóa."""

    def __init__(self, repository: EvolutionRepository) -> None:
        self.repository = repository

    def execute(
        self, request: ProposeEvolutionRequest, evidences: list[Evidence]
    ) -> EvolutionObject:
        metadata = Metadata(
            environment=request.environment,
            criticality=request.criticality,
        )
        provenance = Provenance(
            author=request.author,
            triggered_by=request.triggered_by,
            parent_id=request.parent_id,
        )
        obj = EvolutionObject(
            id=request.id,
            name=request.name,
            payload=request.payload,
            metadata=metadata,
            provenance=provenance,
            evidences=evidences,
        )
        return self.repository.save(obj)