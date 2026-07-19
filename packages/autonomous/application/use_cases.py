import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel  # Nhập khẩu BaseModel

from packages.autonomous.domain.models import LoopCycle
from packages.autonomous.domain.ports import AutonomousRepository
from packages.evolution.application.use_cases import (
    ProposeEvolutionRequest,  # Nhập khẩu ProposeEvolutionRequest
    ProposeEvolutionUseCase,
)


class LoopCycleRequest(BaseModel):
    problem: str
    author: str


class RunAutonomousLoopUseCase:
    """Application Service điều phối vòng lặp tiến hóa đóng kín 13 mắt xích."""

    def __init__(self, repo: AutonomousRepository, services: dict[str, Any]) -> None:
        self.repo = repo
        self.services = services

    def execute(self, request: LoopCycleRequest) -> LoopCycle:
        cycle_id = f"CYC-{uuid.uuid4().hex[:6].upper()}"
        stage_executions: dict[str, str] = {}

        # 1. KNOWLEDGE
        knowledge_repo = self.services["knowledge_repo"]
        doc = knowledge_repo.find_by_id("MEM-2028-FAIL")
        stage_executions["Knowledge"] = (
            f"Read Baseline: {doc.id if doc else 'Genesis'}"
        )

        # 2. MEMORY
        memory_repo = self.services["memory_repo"]
        recalled = memory_repo.vector_search("Splay RAM", limit=1)
        recalled_id = recalled[0].id if recalled else "None"
        stage_executions["Memory"] = f"Recalled Failures: {recalled_id}"

        # 3. REASONING
        from packages.intelligence.application.use_cases import (
            ReasoningRequest,
            RunEcosystemIntelligenceUseCase,
        )
        intelligence_registry = self.services["intelligence_registry"]
        intel_uc = RunEcosystemIntelligenceUseCase(intelligence_registry)
        
        reason_req = ReasoningRequest(
            goal=request.problem, confidence_threshold=0.90
        )
        decision = intel_uc.evaluate_reasoning_and_decide(
            reason_req,
            {
                "knowledge_repo": knowledge_repo,
                "memory_repo": memory_repo,
            }
        )
        stage_executions["Reasoning"] = f"Decision Made: {decision.id}"

        # 4. PLANNING
        from packages.intelligence.application.use_cases import PlanRequest
        plan_req = PlanRequest(
            goal_description=request.problem, assigned_agent="CoderAgent"
        )
        plan = intel_uc.generate_ecosystem_plan(
            plan_req, {"workflow_registry": self.services["workflow_registry"]}
        )
        stage_executions["Planning"] = f"Plan Generated: {plan.id}"

        # 5. WORKFLOW & 6. EXECUTION
        from packages.workflow.application.use_cases import (
            ExecuteWorkflowUseCase,
            StartWorkflowRequest,
        )
        workflow_registry = self.services["workflow_registry"]
        wf_uc = ExecuteWorkflowUseCase(workflow_registry)
        
        wf_instance = wf_uc.start_workflow(
            StartWorkflowRequest(workflow_id=plan.compiled_workflow_id)
        )
        stage_executions["Workflow"] = f"FSM Compiled: {wf_instance.workflow_id}"
        stage_executions["Execution"] = f"FSM Executed: {wf_instance.instance_id}"

        # 7. REFLECTION
        from packages.reflection.application.use_cases import AnalyzeReflectionUseCase
        reflection_repo = self.services["reflection_repo"]
        ref_uc = AnalyzeReflectionUseCase(reflection_repo)
        report = ref_uc.execute(
            subject_id=plan.compiled_workflow_id,
            trigger_event="Simulated Execution Failure",
            passed_checks=False,
        )
        stage_executions["Reflection"] = f"Diagnosed: {report.id}"

        # 8. LEARNING
        from packages.learning.application.use_cases import IngestLearningUseCase
        learning_repo = self.services["learning_repo"]
        learn_uc = IngestLearningUseCase(learning_repo, reflection_repo)
        exp = learn_uc.execute(report.id)
        stage_executions["Learning"] = f"Ingested Experience: {exp.id}"

        # 9. EVOLUTION
        from packages.evolution.application.use_cases import MigrateEvolutionUseCase
        evolution_repo = self.services["evolution_repo"]
        evolve_uc = MigrateEvolutionUseCase(evolution_repo)
        evo_council = self.services["evo_council"]
        propose_uc = ProposeEvolutionUseCase(evolution_repo, evo_council)
        
        base_obj = propose_uc.execute(
            ProposeEvolutionRequest(
                id="EVO-HEAL-TARGET",
                name="Target System",
                payload={"max_retry_loops": 10},
                author="ArchitectAgent",
                triggered_by="Initial Setup",
            ),
            votes=[]
        )
        
        migrated = evolve_uc.execute_migration(
            doc_id=base_obj.id,
            migration_rules={"max_retry_loops": "default:5"},
            author="SelfEvolutionEngine",
        )
        stage_executions["Evolution"] = f"Committed: {migrated.version.to_string()}"

        # 10. FEDERATION (Dọn dẹp biến thừa)
        stage_executions["Federation"] = "Federation Member: Enterprise-B"

        # 11. NEGOTIATION
        from packages.civilization.application.use_cases import (
            ExecuteCivilizationCivilianUseCase,
            NegotiationRequest,
        )
        civilization_repo = self.services["civilization_repo"]
        civ_uc = ExecuteCivilizationCivilianUseCase(civilization_repo)
        
        neg = civ_uc.negotiate_capability_exchange(
            NegotiationRequest(
                offering_member_id="Enterprise-A",
                demanding_member_id="Enterprise-B",
                capability_exchanged="capability.identity",
                cost_tokens=1000.0,
            )
        )
        stage_executions["Negotiation"] = f"Agreement: {neg.status}"

        # 12. CONSENSUS & 13. EVOLUTION LEDGER
        from packages.civilization.application.use_cases import ConsensusRequest
        tx = civ_uc.commit_global_consensus(
            ConsensusRequest(
                proposal_id=neg.id,
                approvals_count=2,
                total_participants=2,
            )
        )
        stage_executions["Consensus"] = f"Consensus status: {tx.status}"
        
        latest_block = civilization_repo.get_latest_block()
        stage_executions["Evolution Ledger"] = f"Mined Block: {latest_block.index}"

        cycle = LoopCycle(
            cycle_id=cycle_id,
            status="SUCCESS",
            stage_executions=stage_executions,
            timestamp=datetime.now(UTC),
        )

        return self.repo.save(cycle)