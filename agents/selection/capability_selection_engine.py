"""Task-to-Capability Selection Engine matching task intents to specialized agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from agents.governance.authority_binding import AuthorityBindingModel
from agents.registry.agent_capability_registry import (
    AgentCapabilityRegistry,
    AgentProfileDTO,
)
from digitaltwin.models.canonical_graph_model import BlastRadiusCategory


@dataclass(frozen=True)
class AgentSelectionDecisionDTO:
    """Decision output of the capability selection engine."""

    task_id: str
    intent: str
    required_authority: str
    blast_radius: BlastRadiusCategory
    matched_capability_ids: list[str]
    primary_implementer_agent: AgentProfileDTO | None
    independent_verifier_agent: AgentProfileDTO | None
    requires_independent_verification: bool
    is_blocked_by_governance: bool
    blocking_reason: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class CapabilitySelectionEngine:
    """Selects specialized implementer and verifier agents based on capability match, authority, and blast radius."""

    def __init__(self, registry: AgentCapabilityRegistry | None = None) -> None:
        self.registry = registry or AgentCapabilityRegistry()

    def select_agents_for_task(
        self,
        task_id: str,
        intent: str,
        task_type: str,
        required_authority: str,
        blast_radius: BlastRadiusCategory = BlastRadiusCategory.LOCAL,
    ) -> AgentSelectionDecisionDTO:
        """Executes full capability matching and agent selection pipeline."""
        # 1. Check L6/L7 Governance Gate
        parsed_auth = AuthorityBindingModel.parse_level(required_authority)
        if parsed_auth >= 6 or blast_radius == BlastRadiusCategory.SYSTEMIC:
            reason = (
                f"Task requires '{required_authority}' authority or "
                "touches SYSTEMIC blast radius. Human ADR approval required."
            )
            return AgentSelectionDecisionDTO(
                task_id=task_id,
                intent=intent,
                required_authority=required_authority,
                blast_radius=blast_radius,
                matched_capability_ids=[],
                primary_implementer_agent=None,
                independent_verifier_agent=None,
                requires_independent_verification=True,
                is_blocked_by_governance=True,
                blocking_reason=reason,
            )

        # 2. Match Capabilities
        matched_caps = [
            cap
            for cap in self.registry.list_all_capabilities()
            if task_type in cap.supported_task_types
            and AuthorityBindingModel.is_authorized(cap.max_authority_level, required_authority)
        ]
        matched_cap_ids = [c.capability_id for c in matched_caps]

        # 3. Select Primary Implementer Agent
        all_agents = self.registry.list_all_agents()
        primary_agent = next(
            (
                a
                for a in all_agents
                if a.role.value == "IMPLEMENTER"
                and AuthorityBindingModel.is_authorized(a.max_authority_level, required_authority)
                and any(c_id in a.capabilities for c_id in matched_cap_ids)
            ),
            None,
        )

        # Fallback to any capable agent if role mismatch
        if not primary_agent:
            primary_agent = next(
                (
                    a
                    for a in all_agents
                    if AuthorityBindingModel.is_authorized(a.max_authority_level, required_authority)
                ),
                None,
            )

        # 4. Determine Independent Verification Requirement
        requires_independent = blast_radius in (
            BlastRadiusCategory.BROAD,
            BlastRadiusCategory.MASS,
        ) or required_authority in ("L4", "L5")

        # 5. Select Independent Verifier Agent
        verifier_agent = None
        if requires_independent:
            verifier_agent = next(
                (
                    a
                    for a in all_agents
                    if a.role.value == "VERIFIER" and a.agent_id != getattr(primary_agent, "agent_id", None)
                ),
                None,
            )

        return AgentSelectionDecisionDTO(
            task_id=task_id,
            intent=intent,
            required_authority=required_authority,
            blast_radius=blast_radius,
            matched_capability_ids=matched_cap_ids,
            primary_implementer_agent=primary_agent,
            independent_verifier_agent=verifier_agent,
            requires_independent_verification=requires_independent,
            is_blocked_by_governance=False,
        )
