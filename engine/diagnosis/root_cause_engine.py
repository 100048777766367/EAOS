"""Causal Reasoning & Root-Cause Engine for EAOS Autonomous Loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class CausalChainDTO:
    """Represents a single causal chain from symptom to root cause."""

    symptom: str
    intermediate_cause: str
    root_cause: str
    affected_component: str
    confidence: float = 1.0


@dataclass(frozen=True)
class DiagnosisReportDTO:
    """Comprehensive diagnosis report clustering failure symptoms into causal groups."""

    diagnosis_id: str
    primary_root_cause: str
    causal_chains: list[CausalChainDTO]
    affected_components: list[str]
    symptoms_clustered_count: int
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class RootCauseEngine:
    """Clusters failure symptoms and diagnoses underlying root causes."""

    def diagnose_failures(self, symptoms: list[str], target_component: str = "general") -> DiagnosisReportDTO:
        """Clusters failure symptoms into causal chains and extracts root causes."""
        import uuid

        diag_id = f"diag-{uuid.uuid4().hex[:8]}"

        if not symptoms:
            return DiagnosisReportDTO(
                diagnosis_id=diag_id,
                primary_root_cause="NO_FAILURE_DETECTED",
                causal_chains=[],
                affected_components=[target_component],
                symptoms_clustered_count=0,
            )

        chains: list[CausalChainDTO] = []
        for sym in symptoms:
            s_lower = sym.lower()
            if "port" in s_lower or "connection" in s_lower or "websocket" in s_lower:
                chains.append(
                    CausalChainDTO(
                        symptom=sym,
                        intermediate_cause="TCP socket listener mismatch or port configuration conflict",
                        root_cause="PORT_OR_RUNTIME_CONFIG_MISMATCH",
                        affected_component="apps/api/app/routers/chat.py",
                    )
                )
            elif "import" in s_lower or "module" in s_lower or "syntax" in s_lower:
                chains.append(
                    CausalChainDTO(
                        symptom=sym,
                        intermediate_cause="Broken module import dependency or missing symbol",
                        root_cause="MISSING_DEPENDENCY_OR_IMPORT_DRIFT",
                        affected_component=target_component,
                    )
                )
            else:
                chains.append(
                    CausalChainDTO(
                        symptom=sym,
                        intermediate_cause="Local component state defect",
                        root_cause="LOCAL_LOGIC_DEFECT",
                        affected_component=target_component,
                    )
                )

        primary_rc = chains[0].root_cause if chains else "UNKNOWN_ROOT_CAUSE"
        affected_comps = list({c.affected_component for c in chains})

        return DiagnosisReportDTO(
            diagnosis_id=diag_id,
            primary_root_cause=primary_rc,
            causal_chains=chains,
            affected_components=affected_comps,
            symptoms_clustered_count=len(symptoms),
        )
