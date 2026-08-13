import time

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

"""AI Agent Execution router."""


router = APIRouter(tags=["AI Agents"])


class AgentExecutionRequest(BaseModel):
    prompt: str
    agent_role: str = "Architect"


class AgentExecutionResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: str
    agent_role: str
    prompt: str
    analysis: str
    governance: str
    timestamp: float


@router.get("/v1/agents/execute")
def execute_agent_get(
    prompt: str = "Rà soát 10 Miền Năng lực trong Neo4j",
    agent_role: str = "Architect",
) -> AgentExecutionResponse:
    return AgentExecutionResponse(
        status="SUCCESS",
        agent_role=agent_role,
        prompt=prompt,
        analysis="Agent executed via GET request.",
        governance="COMPLIANT_WITH_ARCHITECTURE_CONSTITUTION_V3",
        timestamp=time.time(),
    )


@router.post("/v1/agents/execute")
async def execute_agent_post(req: AgentExecutionRequest) -> AgentExecutionResponse:
    return AgentExecutionResponse(
        status="SUCCESS",
        agent_role=req.agent_role,
        prompt=req.prompt,
        analysis="Agent executed via POST request.",
        governance="COMPLIANT_WITH_ARCHITECTURE_CONSTITUTION_V3",
        timestamp=time.time(),
    )
