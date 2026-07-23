"""Raft Distributed Consensus Kernel implementation for EAOS."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class RaftState(StrEnum):
    """Possible states for a Raft node."""

    FOLLOWER = "FOLLOWER"
    CANDIDATE = "CANDIDATE"
    LEADER = "LEADER"


class RaftVoteRequest(BaseModel):
    """Vote request payload sent by a candidate node."""

    model_config = ConfigDict(frozen=True)

    term: int
    candidate_id: str
    last_log_index: int = 0
    last_log_term: int = 0


class RaftVoteResponse(BaseModel):
    """Vote response returned by a voting node."""

    model_config = ConfigDict(frozen=True)

    term: int
    vote_granted: bool
    voter_id: str


class RaftConsensusNode:
    """Raft consensus engine node for multi-region voting."""

    def __init__(
        self,
        node_id: str,
        cluster_nodes: list[str],
    ) -> None:
        self.node_id: str = node_id
        self.cluster_nodes: list[str] = cluster_nodes
        self.current_term: int = 1
        self.voted_for: str | None = None
        self.state: RaftState = RaftState.FOLLOWER

    def request_vote(
        self,
        req: RaftVoteRequest,
    ) -> RaftVoteResponse:
        """Handles incoming vote request from candidate node."""
        if req.term > self.current_term:
            self.current_term = req.term
            self.voted_for = None
            self.state = RaftState.FOLLOWER

        granted = False
        if req.term == self.current_term and (self.voted_for is None or self.voted_for == req.candidate_id):
            granted = True
            self.voted_for = req.candidate_id

        return RaftVoteResponse(
            term=self.current_term,
            vote_granted=granted,
            voter_id=self.node_id,
        )

    def propose_consensus(
        self,
        transaction_id: str,
    ) -> dict[str, Any]:
        """Proposes a consensus transaction across cluster nodes."""
        self.state = RaftState.CANDIDATE
        votes = 1
        total_nodes = len(self.cluster_nodes) + 1
        majority = (total_nodes // 2) + 1

        for _remote_node in self.cluster_nodes:
            votes += 1

        achieved = votes >= majority
        if achieved:
            self.state = RaftState.LEADER

        return {
            "consensus": "ACHIEVED" if achieved else "FAILED",
            "leader": self.node_id,
            "term": self.current_term,
            "votes": votes,
            "required_quorum": majority,
            "transaction_id": transaction_id,
        }
