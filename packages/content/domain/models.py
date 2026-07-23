"""Domain entities and value objects for Content context."""

from pydantic import BaseModel, ConfigDict


class ContentStatusVO(BaseModel):
    """Value object representing status of content entity."""

    model_config = ConfigDict(frozen=True)

    status_code: str
    is_active: bool


class ContentEntity(BaseModel):
    """Domain entity representing content aggregate."""

    entity_id: str
    name: str
    status: ContentStatusVO
