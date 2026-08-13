"""Federation and Synod Consensus Router."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from kernel.federation.cross_region_sync import CRDTStateSyncEngine
from kernel.federation.raft import RaftConsensusNode
from kernel.federation.synod_protocol import (
    BFTSynodProtocolEngine,
    SynodProposal,
    SynodQuorumResult,
)
from packages.federation.domain.models import EcosystemMember

from apps.api.app.container import federation_registry
from apps.api.app.dto.api_response_dto import RaftProposeRequest

router = APIRouter(prefix="/federation", tags=["Federation"])


@router.get("/members", response_model=list[EcosystemMember])
@router.get("/v1/members", response_model=list[EcosystemMember])
async def v1_list_federation_members() -> list[EcosystemMember]:
    return federation_registry.list_members()


@router.post("/crdt/sync-delta")
async def sync_crdt_delta(
    request: dict[str, Any] | None = None,
    delta: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
) -> dict[str, Any]:
    d_data = delta
    if isinstance(request, dict) and not d_data:
        d_data = request.get("delta", {})

    engine = CRDTStateSyncEngine(node_id="node_us_east_1", region="us-east-1")
    return engine.merge_delta(d_data or {})


@router.post("/raft/propose")
async def propose_raft_consensus(
    request: RaftProposeRequest | dict[str, Any],
) -> dict[str, Any]:
    node_id = str(request.get("node_id", "node_1")) if isinstance(request, dict) else request.node_id
    tx_id = str(request.get("transaction_id", "tx_001")) if isinstance(request, dict) else request.transaction_id

    node = RaftConsensusNode(node_id=node_id, cluster_nodes=["node_2", "node_3"])
    return node.propose_consensus(transaction_id=tx_id)


@router.post("/synod/vote-bft")
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

    engine = BFTSynodProtocolEngine(enterprise_id="enterprise_node_1", total_nodes=4)
    proposal = SynodProposal(
        proposal_id=p_id or "prop_001",
        proposer_enterprise="enterprise_node_1",
        action=act or "SYNC",
        payload_hash="sha256_dummy_hash",
    )
    return engine.propose_governance(proposal=proposal, votes=v_list or [])
