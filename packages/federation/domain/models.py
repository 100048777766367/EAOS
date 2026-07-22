from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class EcosystemMember(BaseModel):
    id: str = Field(..., description="Mã doanh nghiệp")
    name: str = Field(..., description="Tên doanh nghiệp")
    constitution_rules: list[str] = Field(default_factory=list)
    capabilities_index: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class SharedKnowledgePacket(BaseModel):
    sender_id: str
    heuristic_id: str
    rule_of_thumb: str
    metric_value: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class CollectiveEvolutionReport(BaseModel):
    member_id: str
    received_from_id: str
    status: str
    reason: str
    simulated_score: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class FederatedCouncilVote(BaseModel):
    voter_member_id: str
    voter_agent_role: str
    decision: str
    reason: str
    voted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class FederatedTransaction(BaseModel):
    tx_id: str
    target_ontology_id: str
    status: str
    votes: list[FederatedCouncilVote] = Field(default_factory=list)
    committed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
