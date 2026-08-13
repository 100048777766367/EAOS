"""Canonical Agent Capability Registry describing specialized capabilities and agent definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from agents.taxonomy.capability_taxonomy import AgentRoleCategory, CapabilityCategory


@dataclass(frozen=True)
class AgentCapabilityDefinitionDTO:
    """Canonical representation of an EAOS Agent Capability."""

    capability_id: str
    capability_name: str
    category: CapabilityCategory
    supported_task_types: list[str]
    max_authority_level: str  # L0 to L7
    allowed_tools: list[str]
    allowed_filesystem_scope: list[str]
    allowed_runtime_scope: list[str]
    input_contract_schema: str
    output_contract_schema: str
    verification_requirements: list[str]
    security_constraints: list[str]
    escalation_conditions: list[str]
    is_active: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentProfileDTO:
    """Canonical representation of an EAOS Specialized Agent."""

    agent_id: str
    agent_name: str
    role: AgentRoleCategory
    capabilities: list[str]  # References capability_ids
    max_authority_level: str
    filesystem_scope: list[str]
    status: str = "ACTIVE"


class AgentCapabilityRegistry:
    """Canonical Registry managing all EAOS specialized agent capability definitions."""

    def __init__(self) -> None:
        self._capabilities: dict[str, AgentCapabilityDefinitionDTO] = {}
        self._agents: dict[str, AgentProfileDTO] = {}
        self._register_default_capabilities()
        self._register_default_agents()

    def register_capability(self, cap: AgentCapabilityDefinitionDTO) -> None:
        """Registers or updates a capability definition."""
        self._capabilities[cap.capability_id] = cap

    def register_agent(self, agent: AgentProfileDTO) -> None:
        """Registers or updates an agent profile."""
        self._agents[agent.agent_id] = agent

    def get_capability(self, cap_id: str) -> AgentCapabilityDefinitionDTO | None:
        """Retrieves capability definition by ID."""
        return self._capabilities.get(cap_id)

    def get_agent(self, agent_id: str) -> AgentProfileDTO | None:
        """Retrieves agent profile by ID."""
        return self._agents.get(agent_id)

    def list_all_capabilities(self) -> list[AgentCapabilityDefinitionDTO]:
        """Lists all registered capability definitions."""
        return list(self._capabilities.values())

    def list_all_agents(self) -> list[AgentProfileDTO]:
        """Lists all registered agent profiles."""
        return list(self._agents.values())

    def _register_default_capabilities(self) -> None:
        """Populates standard EAOS capabilities."""
        self.register_capability(
            AgentCapabilityDefinitionDTO(
                capability_id="cap-repo-inspection",
                capability_name="Repository Inspection & AST Scan",
                category=CapabilityCategory.CODE_ANALYSIS,
                supported_task_types=["inspection", "dependency_scan", "ast_parse"],
                max_authority_level="L1",
                allowed_tools=["list_dir", "view_file", "grep_search"],
                allowed_filesystem_scope=["*"],
                allowed_runtime_scope=["read_only"],
                input_contract_schema="TaskInputSchema",
                output_contract_schema="AnalysisReportSchema",
                verification_requirements=["ast_validity"],
                security_constraints=["read_only_mode"],
                escalation_conditions=["corrupted_file"],
            )
        )

        self.register_capability(
            AgentCapabilityDefinitionDTO(
                capability_id="cap-code-patching",
                capability_name="Local Code Patching",
                category=CapabilityCategory.CODE_MODIFICATION,
                supported_task_types=["patch", "bug_fix", "local_edit"],
                max_authority_level="L2",
                allowed_tools=["replace_file_content", "multi_replace_file_content", "write_to_file"],
                allowed_filesystem_scope=["apps/", "packages/", "runtime/"],
                allowed_runtime_scope=["local_workspace"],
                input_contract_schema="PatchTaskSchema",
                output_contract_schema="PatchDiffSchema",
                verification_requirements=["pytest_unit"],
                security_constraints=["no_secret_commit", "workspace_boundary_only"],
                escalation_conditions=["blast_radius_exceeded", "l6_architecture_crossing"],
            )
        )

        self.register_capability(
            AgentCapabilityDefinitionDTO(
                capability_id="cap-implementation-rewrite",
                capability_name="Coherent Implementation Reconstruction",
                category=CapabilityCategory.REWRITE,
                supported_task_types=["rewrite", "reconstruct_implementation"],
                max_authority_level="L4",
                allowed_tools=["write_to_file", "replace_file_content"],
                allowed_filesystem_scope=["apps/", "packages/", "runtime/"],
                allowed_runtime_scope=["sandbox"],
                input_contract_schema="RewriteTaskSchema",
                output_contract_schema="ProofChecklistSchema",
                verification_requirements=["independent_verifier_gate", "full_test_suite"],
                security_constraints=["proof_checklist_mandatory"],
                escalation_conditions=["contract_drift", "l6_boundary_change"],
            )
        )

        self.register_capability(
            AgentCapabilityDefinitionDTO(
                capability_id="cap-repository-recovery",
                capability_name="Repository Integrity Restoration",
                category=CapabilityCategory.RECOVERY,
                supported_task_types=["recovery", "restore_git_baseline"],
                max_authority_level="L5",
                allowed_tools=["run_command", "write_to_file"],
                allowed_filesystem_scope=["*"],
                allowed_runtime_scope=["recovery_mode"],
                input_contract_schema="RecoveryTaskSchema",
                output_contract_schema="IntegrityReportSchema",
                verification_requirements=["git_status_clean", "compile_check"],
                security_constraints=["freeze_mutation_on_start"],
                escalation_conditions=["unrecoverable_corruption"],
            )
        )

        self.register_capability(
            AgentCapabilityDefinitionDTO(
                capability_id="cap-independent-verification",
                capability_name="Independent Verification & Evidence Proof",
                category=CapabilityCategory.VERIFICATION,
                supported_task_types=["verify", "audit_proof", "quality_gate"],
                max_authority_level="L3",
                allowed_tools=["run_command", "view_file"],
                allowed_filesystem_scope=["*"],
                allowed_runtime_scope=["read_only"],
                input_contract_schema="VerificationInputSchema",
                output_contract_schema="EvidenceProofSchema",
                verification_requirements=["reproducible_test_run"],
                security_constraints=["zero_trust_agent_claims"],
                escalation_conditions=["verification_failed"],
            )
        )

    def _register_default_agents(self) -> None:
        """Populates standard EAOS specialized agents."""
        self.register_agent(
            AgentProfileDTO(
                agent_id="agent-repository-engineer",
                agent_name="Repository Engineer",
                role=AgentRoleCategory.IMPLEMENTER,
                capabilities=["cap-repo-inspection", "cap-code-patching", "cap-implementation-rewrite"],
                max_authority_level="L4",
                filesystem_scope=["apps/", "packages/", "runtime/"],
            )
        )

        self.register_agent(
            AgentProfileDTO(
                agent_id="agent-independent-verifier",
                agent_name="Independent Quality Verifier",
                role=AgentRoleCategory.VERIFIER,
                capabilities=["cap-repo-inspection", "cap-independent-verification"],
                max_authority_level="L3",
                filesystem_scope=["*"],
            )
        )

        self.register_agent(
            AgentProfileDTO(
                agent_id="agent-recovery-guardian",
                agent_name="Repository Recovery Guardian",
                role=AgentRoleCategory.RECOVERY_AGENT,
                capabilities=["cap-repository-recovery"],
                max_authority_level="L5",
                filesystem_scope=["*"],
            )
        )
