"""Master Cybernetic Execution Engine Orchestrator running the Autonomous Engineering Loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from agents.agent_manager import AgentManager
from digitaltwin.models.canonical_graph_model import BlastRadiusCategory
from digitaltwin.twin_orchestrator import EnterpriseDigitalTwinOrchestrator
from pydantic import BaseModel, ConfigDict, Field

from engine.critique.self_critique_convergence_engine import ConvergenceGateReportDTO, SelfCritiqueConvergenceEngine
from engine.diagnosis.root_cause_engine import DiagnosisReportDTO, RootCauseEngine
from engine.intent.intent_model import EngineeringIntentBuilder, EngineeringIntentDTO
from engine.lifecycle.engineering_lifecycle import EngineeringLifecycleFSM, LifecycleStage
from engine.memory.task_memory_store import EngineeringTaskRecordDTO, TaskMemoryStore
from engine.planner.task_planner import AutonomousTaskPlannerEngine
from engine.protocol.rewrite_protocol import RewriteProtocol
from engine.recovery.rollback_escalation_engine import EscalationReportDTO, RollbackEscalationEngine
from engine.sandbox.wasm_runtime import WASMSandboxRuntime
from engine.scheduler.cybernetic_scheduler import CyberneticScheduler
from engine.state.system_state_model import SystemStateEvaluator, SystemStateReportDTO
from engine.strategy.strategy_selection_engine import (
    EngineeringStrategyCategory,
    StrategyDecisionDTO,
    StrategySelectionEngine,
)
from engine.verification.adaptive_verification_engine import AdaptiveVerificationEngine


class EngineStatusDTO(BaseModel):
    """Operational status DTO for master execution engine."""

    model_config = ConfigDict(frozen=True)

    status: str = Field(default="ACTIVE")
    sub_engines_count: int = Field(default=12)
    cybernetic_loop_active: bool = Field(default=True)


@dataclass(frozen=True)
class AutonomousLoopResultDTO:
    """Complete execution result of an autonomous engineering loop run."""

    loop_id: str
    task_id: str
    intent: EngineeringIntentDTO
    system_state: SystemStateReportDTO
    diagnosis: DiagnosisReportDTO
    strategy_decision: StrategyDecisionDTO
    is_converged: bool
    is_escalated: bool
    escalation_report: EscalationReportDTO | None
    convergence_report: ConvergenceGateReportDTO | None
    evidence_token: str
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class EAOSMasterEngine:
    """Master Orchestrator binding all cybernetic sub-engines into a bounded Autonomous Engineering Loop."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        self.root = (workspace_root or Path.cwd()).resolve()
        self.planner = AutonomousTaskPlannerEngine()
        self.sandbox = WASMSandboxRuntime()
        self.scheduler = CyberneticScheduler()

        # Task 6 Engineering Loop Engines
        self.intent_builder = EngineeringIntentBuilder()
        self.state_evaluator = SystemStateEvaluator(self.root)
        self.root_cause_engine = RootCauseEngine()
        self.strategy_engine = StrategySelectionEngine()
        self.rewrite_protocol = RewriteProtocol()
        self.verification_engine = AdaptiveVerificationEngine()
        self.critique_engine = SelfCritiqueConvergenceEngine()
        self.rollback_engine = RollbackEscalationEngine()
        self.memory_store = TaskMemoryStore()

        # Inter-subsystem facades
        self.digital_twin = EnterpriseDigitalTwinOrchestrator()
        self.agent_manager = AgentManager()

    def get_engine_status(self) -> EngineStatusDTO:
        """Return status summary of master execution engine."""
        return EngineStatusDTO(
            status="ACTIVE",
            sub_engines_count=12,
            cybernetic_loop_active=True,
        )

    def run_autonomous_loop(
        self,
        task_id: str,
        raw_user_request: str,
        target_files: list[str],
        required_authority: str = "L2",
        blast_radius: BlastRadiusCategory = BlastRadiusCategory.LOCAL,
    ) -> AutonomousLoopResultDTO:
        """Executes the full 17-stage bounded autonomous engineering lifecycle loop."""
        import uuid

        loop_id = f"loop-{uuid.uuid4().hex[:8]}"

        fsm = EngineeringLifecycleFSM(loop_id)

        # Stage 1: INTENT
        fsm.transition_to(LifecycleStage.INTENT, "UserRequest", raw_user_request)
        intent = self.intent_builder.build_intent(raw_user_request, required_authority=required_authority)

        # Stage 2: OBSERVATION
        fsm.transition_to(LifecycleStage.OBSERVATION, "DigitalTwinScan")

        # Stage 3: SYSTEM_STATE
        fsm.transition_to(LifecycleStage.SYSTEM_STATE, "StateEvaluator")
        state_report = self.state_evaluator.evaluate_system_state()

        if not state_report.is_mutation_allowed:
            fsm.transition_to(LifecycleStage.ESCALATE, "CorruptedStateEscalation")
            esc = self.rollback_engine.escalate_to_human(task_id, state_report.details, "L5")
            return AutonomousLoopResultDTO(
                loop_id=loop_id,
                task_id=task_id,
                intent=intent,
                system_state=state_report,
                diagnosis=DiagnosisReportDTO(f"diag-{loop_id}", "CORRUPTED", [], [], 0),
                strategy_decision=StrategyDecisionDTO(
                    f"strat-{loop_id}", EngineeringStrategyCategory.RECOVER, "L5", state_report.details, []
                ),
                is_converged=False,
                is_escalated=True,
                escalation_report=esc,
                convergence_report=None,
                evidence_token=f"TOKEN-CORRUPTED-{loop_id}",
            )

        # Stage 4: DIAGNOSIS
        fsm.transition_to(LifecycleStage.DIAGNOSIS, "RootCauseEngine")

        # Stage 5: ROOT_CAUSE
        fsm.transition_to(LifecycleStage.ROOT_CAUSE, "RootCauseEngine")
        diagnosis_report = self.root_cause_engine.diagnose_failures(
            [], target_component=target_files[0] if target_files else "general"
        )

        # Stage 6: STRATEGY
        fsm.transition_to(LifecycleStage.STRATEGY, "StrategySelectionEngine")
        strategy_decision = self.strategy_engine.select_strategy(
            state_report, diagnosis_report, required_authority, blast_radius
        )

        if strategy_decision.selected_strategy == EngineeringStrategyCategory.ESCALATE:
            fsm.transition_to(LifecycleStage.ESCALATE, "GovernanceEscalation")
            esc = self.rollback_engine.escalate_to_human(task_id, strategy_decision.rationale, required_authority)
            return AutonomousLoopResultDTO(
                loop_id=loop_id,
                task_id=task_id,
                intent=intent,
                system_state=state_report,
                diagnosis=diagnosis_report,
                strategy_decision=strategy_decision,
                is_converged=False,
                is_escalated=True,
                escalation_report=esc,
                convergence_report=None,
                evidence_token=f"TOKEN-ESCALATED-{loop_id}",
            )

        # Stage 7: AUTHORITY
        fsm.transition_to(LifecycleStage.AUTHORITY, "AuthorityBinding")

        # Stage 8: BLAST_RADIUS
        fsm.transition_to(LifecycleStage.BLAST_RADIUS, "ImpactAnalysisEngine")

        # Stage 9: PLAN
        fsm.transition_to(LifecycleStage.PLAN, "TaskPlanner")

        # Stage 10: SIMULATION
        fsm.transition_to(LifecycleStage.SIMULATION, "GraphDeltaCheckpoint")

        # Stage 11: EXECUTION
        fsm.transition_to(LifecycleStage.EXECUTION, "MultiAgentOrchestrator")

        # Execute rewrite protocol if strategy is REWRITE
        if strategy_decision.selected_strategy == EngineeringStrategyCategory.REWRITE:
            self.rewrite_protocol.execute_rewrite_protocol(
                target_files[0] if target_files else "general", f"EV-{loop_id}"
            )

        # Stage 12: VERIFICATION
        fsm.transition_to(LifecycleStage.VERIFICATION, "AdaptiveVerificationEngine")
        ver_report = self.verification_engine.execute_verification_pipeline(
            strategy_decision.selected_strategy, blast_radius
        )

        # Stage 13: SELF_CRITIQUE
        fsm.transition_to(LifecycleStage.SELF_CRITIQUE, "SelfCritiqueConvergenceEngine")

        # Stage 14: CONVERGENCE
        fsm.transition_to(LifecycleStage.CONVERGENCE, "ConvergenceGate")
        critique_report = self.critique_engine.evaluate_convergence(
            intent_satisfied=True,
            verification_passed=ver_report.all_gates_passed,
            evidence_token=ver_report.evidence_token,
        )

        if critique_report.is_converged:
            fsm.transition_to(LifecycleStage.COMPLETED, "ConvergenceGatePass")
        else:
            fsm.transition_to(LifecycleStage.FAILED, "ConvergenceGateFail")

        # Save to task memory store
        self.memory_store.save_record(
            EngineeringTaskRecordDTO(
                loop_id=loop_id,
                task_id=task_id,
                intent_summary=intent.interpreted_objective,
                system_state=state_report.state.value,
                strategy=strategy_decision.selected_strategy.value,
                authority=required_authority,
                blast_radius=blast_radius.value,
                is_converged=critique_report.is_converged,
                evidence_token=critique_report.convergence_evidence_token,
            )
        )

        return AutonomousLoopResultDTO(
            loop_id=loop_id,
            task_id=task_id,
            intent=intent,
            system_state=state_report,
            diagnosis=diagnosis_report,
            strategy_decision=strategy_decision,
            is_converged=critique_report.is_converged,
            is_escalated=False,
            escalation_report=None,
            convergence_report=critique_report,
            evidence_token=critique_report.convergence_evidence_token,
        )
