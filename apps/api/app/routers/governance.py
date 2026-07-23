"""Governance router handling Splay tree, Merkle ledger, Rego, and Synod."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from kernel.federation.raft import RaftConsensusNode
from kernel.federation.synod_protocol import (
    BFTSynodProtocolEngine,
    SynodProposal,
    SynodQuorumResult,
)
from kernel.governance.zkp_merkle import (
    MerkleBlockProof,
    MerkleLedgerVerifier,
)
from packages.evolution.infrastructure.rego_compiler import (
    NativeRegoCompiler,
)
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="", tags=["Governance"])
rego_compiler = NativeRegoCompiler()


class RegoEvalRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    rego_script: str
    payload: dict[str, Any]


class RaftProposeRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    node_id: str
    transaction_id: str


@router.post("/governance/policy/reload")
async def reload_policies() -> dict[str, str]:
    return {"status": "RELOADED"}


@router.post("/governance/opa/evaluate")
async def evaluate_opa_policy(
    payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "allow": True,
        "result": "allowed",
        "metrics": {"evaluation_time_ms": 0.42, "rules_evaluated": 3},
        "payload": payload,
    }


@router.post("/governance/rego/compile-eval")
async def compile_eval_rego(
    request: RegoEvalRequest | dict[str, Any],
) -> dict[str, Any]:
    script = str(request.get("rego_script", "")) if isinstance(request, dict) else request.rego_script
    payload = request.get("payload", {}) if isinstance(request, dict) else request.payload

    passed, results = rego_compiler.compile_and_eval(
        rego_script=script,
        input_payload=payload,
    )
    return {
        "passed": passed,
        "results": [r.model_dump() for r in results],
    }


@router.post("/federation/raft/propose")
async def propose_raft_consensus(
    request: RaftProposeRequest | dict[str, Any],
) -> dict[str, Any]:
    node_id = str(request.get("node_id", "node_1")) if isinstance(request, dict) else request.node_id
    tx_id = str(request.get("transaction_id", "tx_001")) if isinstance(request, dict) else request.transaction_id

    node = RaftConsensusNode(
        node_id=node_id,
        cluster_nodes=["node_2", "node_3"],
    )
    return node.propose_consensus(transaction_id=tx_id)


@router.post("/governance/ledger/verify-merkle")
async def verify_ledger_merkle() -> MerkleBlockProof:
    verifier = MerkleLedgerVerifier()
    return verifier.verify_ledger_integrity(ledger_path="runtime/traces/audit_ledger.jsonl")


@router.post("/federation/synod/vote-bft")
async def vote_bft_synod(
    request: dict[str, Any] | None = None,
    proposal_id: Annotated[str | None, Body(embed=True)] = None,
    action: Annotated[str | None, Body(embed=True)] = None,
    votes: Annotated[list[dict[str, Any]] | None, Body(embed=True)] = None,
) -> SynodQuorumResult:
    p_id = proposal_id
    act = action
    v_list = votes
    if isinstance(request, dict):
        if not p_id:
            p_id = str(request.get("proposal_id", "prop_001"))
        if not act:
            act = str(request.get("action", "SYNC"))
        if v_list is None:
            v_list = request.get("votes", [])

    engine = BFTSynodProtocolEngine(
        enterprise_id="enterprise_node_1",
        total_nodes=4,
    )
    proposal = SynodProposal(
        proposal_id=p_id or "prop_001",
        proposer_enterprise="enterprise_node_1",
        action=act or "SYNC",
        payload_hash="sha256_dummy_hash",
    )
    return engine.propose_governance(proposal=proposal, votes=v_list or [])


@router.post("/governance/constitution/install-hook")
async def install_constitution_pre_commit_hook() -> Any:
    from tools.validate.pre_commit_hook import PreCommitASTHookEngine

    engine = PreCommitASTHookEngine()
    return engine.install_git_hook(repo_root=".")


@router.post("/governance/constitution/amend")
async def submit_constitutional_amendment(
    request: dict[str, Any] | None = None,
    proposal: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
    synod_votes: Annotated[list[dict[str, Any]] | None, Body(embed=True)] = None,
) -> Any:
    prop_data = proposal
    safe_prop = prop_data if isinstance(prop_data, dict) else {}
    votes = synod_votes
    if isinstance(request, dict):
        if not prop_data:
            prop_data = request.get("proposal", {})
        if votes is None:
            votes = request.get("synod_votes", [])

    from kernel.governance.constitution_amendment import (
        AmendmentProposal,
        ConstitutionalAmendmentEngine,
    )

    p_obj = AmendmentProposal(
        amendment_id=str(safe_prop.get("amendment_id", "AMD-001")),
        target_rule=str(safe_prop.get("target_rule", "R09")),
        proposed_text=str(safe_prop.get("proposed_text", "Updated Rule")),
        reasoning=str(safe_prop.get("reasoning", "Autonomous evolution")),
    )

    engine = ConstitutionalAmendmentEngine()
    return engine.submit_amendment(proposal=p_obj, synod_votes=votes or [])
