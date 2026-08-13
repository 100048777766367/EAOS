"""Agent Supervisor Engine tracking active agents, failure classifications, and zero-trust verification."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class AgentFailureCategory(StrEnum):
    """Canonical Classification of Agent Failures."""

    AGENT_TIMEOUT = "AGENT_TIMEOUT"
    AGENT_CRASH = "AGENT_CRASH"
    AGENT_PROTOCOL_FAILURE = "AGENT_PROTOCOL_FAILURE"
    CAPABILITY_MISMATCH = "CAPABILITY_MISMATCH"
    AUTHORITY_DENIED = "AUTHORITY_DENIED"
    TOOL_FAILURE = "TOOL_FAILURE"
    CONTEXT_FAILURE = "CONTEXT_FAILURE"
    CONFLICTING_AGENT = "CONFLICTING_AGENT"
    SECURITY_BLOCK = "SECURITY_BLOCK"
    VERIFICATION_FAILURE = "VERIFICATION_FAILURE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ActiveAgentTelemetryDTO:
    """Live observation telemetry for a supervised agent."""

    agent_id: str
    assigned_task_id: str
    status: str  # IDLE, EXECUTING, VERIFYING, BLOCKED, FAILED
    authority_level: str
    files_touched: list[str]
    locks_held: list[str]
    last_action: str
    last_updated: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass(frozen=True)
class AgentClaimVerificationDTO:
    """Result of evaluating an agent's completion claim against zero-trust evidence rules."""

    agent_id: str
    task_id: str
    claimed_success: bool
    evidence_provided: bool
    independent_verification_passed: bool
    claim_accepted: bool
    reason: str


class AgentSupervisor:
    """Supervises active agents, tracks telemetry, classifies failures, and enforces zero-trust claim rules."""

    def __init__(self) -> None:
        self._telemetry: dict[str, ActiveAgentTelemetryDTO] = {}

    def update_agent_telemetry(
        self,
        agent_id: str,
        task_id: str,
        status: str,
        authority_level: str,
        files_touched: list[str],
        locks_held: list[str],
        last_action: str,
    ) -> ActiveAgentTelemetryDTO:
        """Updates live observation telemetry for an active agent."""
        t = ActiveAgentTelemetryDTO(
            agent_id=agent_id,
            assigned_task_id=task_id,
            status=status,
            authority_level=authority_level,
            files_touched=files_touched,
            locks_held=locks_held,
            last_action=last_action,
        )
        self._telemetry[agent_id] = t
        return t

    def get_agent_telemetry(self, agent_id: str) -> ActiveAgentTelemetryDTO | None:
        """Retrieves live telemetry for an agent."""
        return self._telemetry.get(agent_id)

    def list_all_active_telemetry(self) -> list[ActiveAgentTelemetryDTO]:
        """Lists live telemetry for all supervised agents."""
        return list(self._telemetry.values())

    def evaluate_completion_claim(
        self,
        agent_id: str,
        task_id: str,
        claimed_success: bool,
        evidence_token: str,
        independent_verification_passed: bool,
    ) -> AgentClaimVerificationDTO:
        """Enforces Zero-Trust Verification: Rejects claims without independent evidence."""
        has_evidence = bool(evidence_token and evidence_token.strip())
        accepted = claimed_success and has_evidence and independent_verification_passed

        if not claimed_success:
            reason = "Agent reported task failure"
        elif not has_evidence:
            reason = "Zero-Trust Violation: Agent claim rejected due to missing evidence token"
        elif not independent_verification_passed:
            reason = "Zero-Trust Violation: Agent claim rejected because independent verification failed"
        else:
            reason = "Completion claim accepted with verified evidence token"

        return AgentClaimVerificationDTO(
            agent_id=agent_id,
            task_id=task_id,
            claimed_success=claimed_success,
            evidence_provided=has_evidence,
            independent_verification_passed=independent_verification_passed,
            claim_accepted=accepted,
            reason=reason,
        )

    def classify_agent_failure(self, exc: Exception | str) -> AgentFailureCategory:
        """Classifies agent exception into canonical AgentFailureCategory."""
        msg = str(exc).lower()
        if "timeout" in msg:
            return AgentFailureCategory.AGENT_TIMEOUT
        if "authority" in msg or "permission" in msg:
            return AgentFailureCategory.AUTHORITY_DENIED
        if "conflict" in msg or "lock" in msg:
            return AgentFailureCategory.CONFLICTING_AGENT
        if "security" in msg or "forbidden" in msg:
            return AgentFailureCategory.SECURITY_BLOCK
        if "verification" in msg or "zero-trust" in msg:
            return AgentFailureCategory.VERIFICATION_FAILURE
        if "tool" in msg:
            return AgentFailureCategory.TOOL_FAILURE
        return AgentFailureCategory.AGENT_CRASH
