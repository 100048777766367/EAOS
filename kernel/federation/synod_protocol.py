"""Inter-Enterprise Byzantine Fault Tolerant (BFT) Synod Protocol for EAOS."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class SynodProposal(BaseModel):
    """Value object representing an inter-enterprise governance proposal."""

    model_config = ConfigDict(frozen=True)

    proposal_id: str
    proposer_enterprise: str
    action: str
    payload_hash: str


class SynodQuorumResult(BaseModel):
    """Value object representing BFT consensus voting outcome."""

    model_config = ConfigDict(frozen=True)

    proposal_id: str
    achieved_bft_consensus: bool
    approvals: int
    fault_tolerance_threshold: int


class BFTSynodProtocolEngine:
    """Byzantine Fault Tolerant (BFT) Synod consensus engine."""

    def __init__(
        self,
        enterprise_id: str,
        total_nodes: int = 4,
    ) -> None:
        self.enterprise_id: str = enterprise_id
        self.total_nodes: int = total_nodes

    def propose_governance(
        self,
        proposal: SynodProposal,
        votes: list[dict[str, Any]],
    ) -> SynodQuorumResult:
        """Evaluates votes against BFT threshold (2f + 1) for consensus."""
        fault_tolerance = (self.total_nodes - 1) // 3
        required_approvals = (2 * fault_tolerance) + 1

        approvals = sum(
            1 for vote in votes if vote.get("decision") == "APPROVE" and vote.get("signature_valid") is not False
        )

        achieved = approvals >= required_approvals

        return SynodQuorumResult(
            proposal_id=proposal.proposal_id,
            achieved_bft_consensus=achieved,
            approvals=approvals,
            fault_tolerance_threshold=required_approvals,
        )
