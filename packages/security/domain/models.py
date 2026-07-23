"""Domain entities and value objects for Security context."""

from pydantic import BaseModel, ConfigDict


class SecurityStatusVO(BaseModel):
    """Value object representing status of security entity."""

    model_config = ConfigDict(frozen=True)

    status_code: str
    is_active: bool


class SecurityEntity(BaseModel):
    """Domain entity representing security aggregate."""

    entity_id: str
    name: str
    status: SecurityStatusVO
