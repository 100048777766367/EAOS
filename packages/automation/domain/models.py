"""Domain entities and value objects for Automation context."""

from pydantic import BaseModel, ConfigDict


class AutomationStatusVO(BaseModel):
    """Value object representing status of automation entity."""

    model_config = ConfigDict(frozen=True)

    status_code: str
    is_active: bool


class AutomationEntity(BaseModel):
    """Domain entity representing automation aggregate."""

    entity_id: str
    name: str
    status: AutomationStatusVO
