from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

"""Mô hình DTO cho hệ thống Đồng thuận Liên bang (FEDERATION)."""


class FederationRole(StrEnum):
    """Vai trò nút liên bang."""

    LEADER = "LEADER"
    FOLLOWER = "FOLLOWER"
    VALIDATOR = "VALIDATOR"


@dataclass(frozen=True)
class VectorClockState:
    """Trạng thái Vector Clock CRDT."""

    node_id: str
    counter: int
    clock_map: dict[str, int] = field(default_factory=dict)


@dataclass
class ConsensusProof:
    """Bằng chứng chứng nhận đồng thuận liên bang."""

    consensus_id: str
    accepted: bool
    signers: list[str] = field(default_factory=list)
    proof_hash: str = ""
