"""Validation schema for EAOS i18n translation catalogs."""

from pydantic import BaseModel, ConfigDict, Field


class SystemCatalog(BaseModel):
    """System status and header translations."""

    model_config = ConfigDict(frozen=True)

    title: str
    welcome: str
    status_active: str
    status_offline: str


class AuthCatalog(BaseModel):
    """Authentication and permission translations."""

    model_config = ConfigDict(frozen=True)

    login: str
    logout: str
    register: str
    unauthorized: str


class ControlRoomCatalog(BaseModel):
    """Control Room UI translations."""

    model_config = ConfigDict(frozen=True)

    title: str
    delegate_task: str
    goal_placeholder: str
    autonomy_level: str
    hitl_approval_required: str
    approve: str
    reject: str


class TranslationCatalogSchema(BaseModel):
    """Root validation schema for translation catalogs."""

    model_config = ConfigDict(frozen=True)

    language_code: str
    language_name: str
    system: SystemCatalog
    auth: AuthCatalog
    control_room: ControlRoomCatalog
    custom: dict[str, str] = Field(default_factory=dict)
