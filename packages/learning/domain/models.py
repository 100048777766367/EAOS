from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class Lesson(BaseModel):
    """GiÃ¡ trá»‹ Ä‘Ãºc rÃºt tá»« má»™t sá»± cá»‘ thá»±c táº¿."""

    id: str
    takeaway: str
    action_item: str

    model_config = ConfigDict(frozen=True)


class Pattern(BaseModel):
    """Máº«u thiáº¿t káº¿ chuáº©n Ä‘Æ°á»£c há»‡ thá»‘ng khuyáº¿n khÃ­ch sá»­ dá»¥ng."""

    id: str
    name: str
    description: str

    model_config = ConfigDict(frozen=True)


class AntiPattern(BaseModel):
    """Máº«u pháº£n thiáº¿t káº¿ (chá»‘ng chá»‰ Ä‘á»‹nh) cáº§n trÃ¡nh."""

    id: str
    name: str
    avoid_reason: str

    model_config = ConfigDict(frozen=True)


class Heuristic(BaseModel):
    """Quy táº¯c kinh nghiá»‡m (Rule of thumb) cá»§a cÃ¡c AI Agents."""

    id: str
    rule_of_thumb: str
    applicability: str

    model_config = ConfigDict(frozen=True)


class Experience(BaseModel):
    """Thá»±c thá»ƒ Kinh nghiá»‡m hoÃ n chá»‰nh cá»§a EAOS, Ä‘Ãºc rÃºt tá»« Reflection."""

    id: str
    reflection_id: str
    title: str
    lessons: list[Lesson] = Field(default_factory=list)
    patterns: list[Pattern] = Field(default_factory=list)
    anti_patterns: list[AntiPattern] = Field(default_factory=list)
    heuristics: list[Heuristic] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
