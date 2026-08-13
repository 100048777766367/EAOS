"""Context Compiler assembling 4-Category Context Snapshot (Rule R41)."""

from __future__ import annotations

from provenance.domain.models import VerifiedEvidenceBundleDTO
from pydantic import BaseModel, ConfigDict, Field


class ModelInputSnapshotDTO(BaseModel):
    """Structured input snapshot provided to LLM Reasoning Engine."""

    model_config = ConfigDict(frozen=True)

    user_identity: str = Field(..., description="Enterprise semantic model field description")
    task_context: str = Field(..., description="Enterprise semantic model field description")
    evidence_bundle: VerifiedEvidenceBundleDTO = Field(..., description="Enterprise semantic model field description")
    operational_rules: list[str] = Field(..., description="Enterprise semantic model field description")


class ContextCompiler:
    """Assembles 4-Category Context Snapshot without LLM summaries."""

    def compile_context(
        self,
        user_id: str,
        task_text: str,
        evidence_bundle: VerifiedEvidenceBundleDTO,
    ) -> ModelInputSnapshotDTO:
        """Constructs strict ModelInputSnapshotDTO."""
        return ModelInputSnapshotDTO(
            user_identity=user_id,
            task_context=task_text,
            evidence_bundle=evidence_bundle,
            operational_rules=[
                "Line length < 88 chars strictly",
                "Domain Purity Rule R01",
                "No LLM token spend for retrieval",
            ],
        )
