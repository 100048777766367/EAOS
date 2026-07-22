from pydantic import BaseModel


class StoreMemoryCommand(BaseModel):
    """DTO Ä‘áº§u vÃ o (Input) Ä‘á»ƒ thá»±c thi Use Case ghi nhá»›."""

    decision_id: str
    outcome: str
    evidence_summary: str
    lesson_learned: str
    key_learnings: list[str]


class MemoryResponse(BaseModel):
    """DTO Ä‘áº§u ra (Output) gá»­i vá» cho API Gateway."""

    id: str
    outcome: str
    lesson_learned: str
