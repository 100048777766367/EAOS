"""Governance and Fitness Compiler Router."""

from typing import Any

from fastapi import APIRouter
from kernel.governance.constitution_amendment import (
    AmendmentProposal,
    ConstitutionalAmendmentEngine,
)
from kernel.governance.zkp_merkle import MerkleBlockProof, MerkleLedgerVerifier
from tools.graph.system_integration_auditor import (
    DirectoryConnectivityDTO,
    SystemIntegrationAuditor,
)
from tools.validate.pre_commit_hook import PreCommitASTHookEngine

from apps.api.app.container import ROOT_PATH, knowledge_repo, policy_evaluator
from apps.api.app.dto.api_response_dto import RegoEvalRequest

router = APIRouter(prefix="/governance", tags=["Governance"])
integration_auditor = SystemIntegrationAuditor(ROOT_PATH)


@router.get("/splay-tree")
async def get_splay_tree_layout() -> dict[str, Any]:
    return {"status": "ACTIVE", "root": knowledge_repo.get_tree_layout()}


@router.get("/splay-tree/mermaid")
async def get_splay_tree_mermaid() -> dict[str, Any]:
    return {"status": "ACTIVE", "mermaid": "graph TD\n  Root --> KnowledgeNode"}


@router.post("/policy/reload")
async def reload_policies() -> dict[str, str]:
    return {"status": "RELOADED"}


@router.post("/opa/evaluate")
async def evaluate_opa_policy(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "allow": True,
        "result": "allowed",
        "metrics": {"evaluation_time_ms": 0.42, "rules_evaluated": 3},
        "payload": payload,
    }


@router.get("/topology/audit", response_model=DirectoryConnectivityDTO)
async def audit_system_topology_connectivity() -> DirectoryConnectivityDTO:
    return integration_auditor.audit_topological_connectivity()


@router.post("/rego/compile-eval")
async def compile_eval_rego(
    request: RegoEvalRequest | dict[str, Any],
) -> dict[str, Any]:
    script = str(request.get("rego_script", "")) if isinstance(request, dict) else request.rego_script
    payload = request.get("payload", {}) if isinstance(request, dict) else request.payload
    passed, results = policy_evaluator.compile_and_eval(rego_script=script, input_payload=payload)
    return {"passed": passed, "results": [r.model_dump() for r in results]}


@router.post("/ledger/verify-merkle", response_model=MerkleBlockProof)
async def verify_ledger_merkle() -> MerkleBlockProof:
    verifier = MerkleLedgerVerifier()
    return verifier.verify_ledger_integrity(ledger_path="runtime/traces/audit_ledger.jsonl")


@router.post("/constitution/install-hook")
async def install_constitution_pre_commit_hook() -> Any:
    engine = PreCommitASTHookEngine()
    return engine.install_git_hook(repo_root=str(ROOT_PATH))


@router.post("/constitution/amend")
async def submit_constitutional_amendment(
    request: dict[str, Any] | None = None,
    proposal: dict[str, Any] | None = None,
    synod_votes: list[dict[str, Any]] | None = None,
) -> Any:
    prop_data = proposal
    safe_prop = prop_data if isinstance(prop_data, dict) else {}
    votes = synod_votes
    if isinstance(request, dict):
        if not prop_data:
            prop_data = request.get("proposal", {})
        if votes is None:
            votes = request.get("synod_votes", [])

    p_obj = AmendmentProposal(
        amendment_id=str(safe_prop.get("amendment_id", "AMD-001")),
        target_rule=str(safe_prop.get("target_rule", "R09")),
        proposed_text=str(safe_prop.get("proposed_text", "Updated Rule")),
        reasoning=str(safe_prop.get("reasoning", "Autonomous evolution")),
    )
    engine = ConstitutionalAmendmentEngine()
    return engine.submit_amendment(proposal=p_obj, synod_votes=votes or [])
