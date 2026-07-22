from pydantic import BaseModel, ConfigDict, Field


class AgentConfig(BaseModel):
    model_name: str
    temperature: float = 0.1


class AIAgent(BaseModel):
    id: str
    role: str
    config: AgentConfig
    current_state: str = "INITIALIZED"
    lifecycle_history: list[str] = Field(default_factory=list)
    model_config = ConfigDict(frozen=True)
