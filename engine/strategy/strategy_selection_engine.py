"""Strategy Selection Engine for EAOS Autonomous Engineering Loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from digitaltwin.models.canonical_graph_model import BlastRadiusCategory
from engine.diagnosis.root_cause_engine import DiagnosisReportDTO
from engine.state.system_state_model import SystemHealthCategory, SystemStateReportDTO


class EngineeringStrategyCategory(StrEnum):
    """The 5 Canonical EAOS Engineering Strategies."""

    PATCH = "PATCH"
    REFACTOR = "REFACTOR"
    REWRITE = "REWRITE"
    RECOVER = "RECOVER"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True)
class StrategyDecisionDTO:
    """Decision output of the strategy selection engine."""

    decision_id: str
    selected_strategy: EngineeringStrategyCategory
    required_authority: str
    rationale: str
    evidence_refs: list[str]
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class StrategySelectionEngine:
    """Selects the primary engineering strategy based on system health, diagnosis, authority, and blast radius."""

    def select_strategy(
        self,
        system_state: SystemStateReportDTO,
        diagnosis: DiagnosisReportDTO,
        required_authority: str,
        blast_radius: BlastRadiusCategory = BlastRadiusCategory.LOCAL,
    ) -> StrategyDecisionDTO:
        """Evaluates system state and diagnosis report to select primary strategy."""
        import uuid

        dec_id = f"strat-{uuid.uuid4().hex[:8]}"

        # 1. System state CORRUPTED -> RECOVER Strategy
        if system_state.state == SystemHealthCategory.CORRUPTED:
            return StrategyDecisionDTO(
                decision_id=dec_id,
                selected_strategy=EngineeringStrategyCategory.RECOVER,
                required_authority="L5",
                rationale=("System state is CORRUPTED. Selecting RECOVER strategy to restore repository integrity."),
                evidence_refs=[system_state.details],
            )

        # 2. Authority >= L6 or Blast Radius == SYSTEMIC -> ESCALATE Strategy
        if required_authority in ("L6", "L7") or blast_radius == BlastRadiusCategory.SYSTEMIC:
            return StrategyDecisionDTO(
                decision_id=dec_id,
                selected_strategy=EngineeringStrategyCategory.ESCALATE,
                required_authority=required_authority,
                rationale=(
                    f"Task requires '{required_authority}' authority or SYSTEMIC blast radius. ESCALATE to human ADR."
                ),
                evidence_refs=[diagnosis.primary_root_cause],
            )

        # 3. Required Authority L4 -> REWRITE Strategy
        if required_authority == "L4":
            return StrategyDecisionDTO(
                decision_id=dec_id,
                selected_strategy=EngineeringStrategyCategory.REWRITE,
                required_authority="L4",
                rationale=(
                    "Coherent implementation reconstruction required. "
                    "Selecting REWRITE strategy under L4 rewrite protocol."
                ),
                evidence_refs=[diagnosis.primary_root_cause],
            )

        # 4. Required Authority L3 or Blast Radius == BROAD -> REFACTOR Strategy
        if required_authority == "L3" or blast_radius == BlastRadiusCategory.BROAD:
            return StrategyDecisionDTO(
                decision_id=dec_id,
                selected_strategy=EngineeringStrategyCategory.REFACTOR,
                required_authority="L3",
                rationale=("Structural cleanup required across component boundaries. Selecting REFACTOR strategy."),
                evidence_refs=[diagnosis.primary_root_cause],
            )

        # 5. Default L2 -> PATCH Strategy
        return StrategyDecisionDTO(
            decision_id=dec_id,
            selected_strategy=EngineeringStrategyCategory.PATCH,
            required_authority="L2",
            rationale="Small local defect identified. Selecting PATCH strategy.",
            evidence_refs=[diagnosis.primary_root_cause],
        )
