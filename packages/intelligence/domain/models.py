from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class ReasoningNode(BaseModel):
    step_number: int = Field(default=1)
    logic: str = Field(..., description="Suy luận logic")

    model_config = ConfigDict(frozen=True)


class SemanticDecision(BaseModel):
    id: str = Field(..., description="Mã quyết định")
    goal: str = Field(default="", description="Mục tiêu")
    matched_knowledge_ids: list[str] = Field(default_factory=list)
    recalled_memory_ids: list[str] = Field(default_factory=list)
    policy_constraints: list[str] = Field(default_factory=list)
    reasoning_chain: list[ReasoningNode] = Field(default_factory=list)
    chosen_option: str = Field(..., description="Phương án chốt")
    confidence_score: float = Field(..., description="Điểm tin cậy")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)


class TaskNode(BaseModel):
    id: str
    name: str
    dependencies: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class EcosystemPlan(BaseModel):
    id: str
    goal: str = Field(default="")
    task_graph: list[TaskNode] = Field(default_factory=list)
    compiled_workflow_id: str = Field(default="")

    model_config = ConfigDict(frozen=True)


class OptimizationGoal(BaseModel):
    metric_name: str
    target_value: float
    current_value: float
    analysis_summary: str = Field(default="")
    recommendations: list[str] = Field(default_factory=list)
    simulation_passed: bool = Field(default=False)
    council_approved: bool = Field(default=False)
    applied_parameters: dict[str, float] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)
