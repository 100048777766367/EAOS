"""EAOS Change Strategy Engine."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class ChangeStrategy(StrEnum):
    """The 5 Engineering Change Strategies in EAOS."""

    PATCH = "PATCH"
    REFACTOR = "REFACTOR"
    REWRITE = "REWRITE"
    RECOVER = "RECOVER"
    ESCALATE = "ESCALATE"


class BlastRadiusLevel(StrEnum):
    """Blast Radius Classification."""

    LOCAL = "LOCAL"  # 1-3 files, single component
    SMALL = "SMALL"  # 4-20 files, multiple components
    BROAD = "BROAD"  # 20-100 files, cross-subsystem
    MASS = "MASS"  # 100+ files / >20 syntax errors
    SYSTEMIC = "SYSTEMIC"  # Cross-boundary architecture / security / governance change


class StrategyDecision(BaseModel):
    """Output decision of StrategyEngine."""

    strategy: ChangeStrategy
    blast_radius: BlastRadiusLevel
    root_cause: str
    affected_files_count: int
    syntax_errors_count: int
    is_corrupted: bool
    rationale: str


class StrategyEngine:
    """Strategy Engine calculating optimal strategy from Root Cause and Blast Radius."""

    def determine_strategy(
        self,
        root_cause: str,
        affected_files_count: int,
        syntax_errors_count: int,
        is_corrupted: bool,
        is_architecture_change: bool = False,
    ) -> StrategyDecision:
        """Calculate ChangeStrategy based on empirical parameters."""
        # 1. Determine Blast Radius
        if is_architecture_change:
            blast_radius = BlastRadiusLevel.SYSTEMIC
        elif affected_files_count >= 100 or syntax_errors_count >= 20:
            blast_radius = BlastRadiusLevel.MASS
        elif affected_files_count >= 20:
            blast_radius = BlastRadiusLevel.BROAD
        elif affected_files_count >= 4:
            blast_radius = BlastRadiusLevel.SMALL
        else:
            blast_radius = BlastRadiusLevel.LOCAL

        # 2. Determine Strategy
        if is_architecture_change:
            strategy = ChangeStrategy.ESCALATE
            rationale = "Architecture boundary change requested. Escalating to human authority & ADR proposal."
        elif is_corrupted or syntax_errors_count >= 20:
            strategy = ChangeStrategy.RECOVER
            rationale = (
                f"Repository integrity issue detected ({syntax_errors_count} syntax errors, corrupted={is_corrupted}). "
                "Selecting RECOVER strategy."
            )
        elif blast_radius in (BlastRadiusLevel.BROAD, BlastRadiusLevel.MASS) or "unsound" in root_cause.lower():
            strategy = ChangeStrategy.REWRITE
            rationale = (
                f"Root cause '{root_cause}' or Blast Radius '{blast_radius.value}' indicates broken logic/abstraction. "
                "Selecting REWRITE strategy for coherent reconstruction."
            )
        elif blast_radius == BlastRadiusLevel.SMALL or "structure" in root_cause.lower():
            strategy = ChangeStrategy.REFACTOR
            rationale = (
                f"Root cause '{root_cause}' indicates sound logic but poor structure. Selecting REFACTOR strategy."
            )
        else:
            strategy = ChangeStrategy.PATCH
            rationale = f"Localized defect ({affected_files_count} files). Selecting PATCH strategy."

        return StrategyDecision(
            strategy=strategy,
            blast_radius=blast_radius,
            root_cause=root_cause,
            affected_files_count=affected_files_count,
            syntax_errors_count=syntax_errors_count,
            is_corrupted=is_corrupted,
            rationale=rationale,
        )
