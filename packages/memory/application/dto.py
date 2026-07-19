from pydantic import BaseModel


class StoreMemoryCommand(BaseModel):
    """DTO đầu vào (Input) để thực thi Use Case ghi nhớ."""

    decision_id: str
    outcome: str
    evidence_summary: str
    lesson_learned: str
    key_learnings: list[str]


class MemoryResponse(BaseModel):
    """DTO đầu ra (Output) gửi về cho API Gateway."""

    id: str
    outcome: str
    lesson_learned: str
