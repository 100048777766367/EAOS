from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class Lesson(BaseModel):
    """Giá trị đúc rút từ một sự cố thực tế."""

    id: str
    takeaway: str
    action_item: str

    model_config = ConfigDict(frozen=True)


class Pattern(BaseModel):
    """Mẫu thiết kế chuẩn được hệ thống khuyến khích sử dụng."""

    id: str
    name: str
    description: str

    model_config = ConfigDict(frozen=True)


class AntiPattern(BaseModel):
    """Mẫu phản thiết kế (chống chỉ định) cần tránh."""

    id: str
    name: str
    avoid_reason: str

    model_config = ConfigDict(frozen=True)


class Heuristic(BaseModel):
    """Quy tắc kinh nghiệm (Rule of thumb) của các AI Agents."""

    id: str
    rule_of_thumb: str
    applicability: str

    model_config = ConfigDict(frozen=True)


class Experience(BaseModel):
    """Thực thể Kinh nghiệm hoàn chỉnh của EAOS, đúc rút từ Reflection."""

    id: str
    reflection_id: str
    title: str
    lessons: list[Lesson] = Field(default_factory=list)
    patterns: list[Pattern] = Field(default_factory=list)
    anti_patterns: list[AntiPattern] = Field(default_factory=list)
    heuristics: list[Heuristic] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = ConfigDict(frozen=True)
