"""Domain entities and value objects for Integration context."""

from pydantic import BaseModel, ConfigDict


class IntegrationStatusVO(BaseModel):
    """Value object representing status of integration entity."""

    model_config = ConfigDict(frozen=True)

    status_code: str
    is_active: bool


class IntegrationEntity(BaseModel):
    """Domain entity representing integration aggregate."""

    entity_id: str
    name: str
    status: IntegrationStatusVO
