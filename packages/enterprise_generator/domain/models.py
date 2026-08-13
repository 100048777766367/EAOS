from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

"""Enterprise Generator Domain Models for EAOS."""


class EnterpriseBlueprintSpec(BaseModel):
    """Value object representing target enterprise specification."""

    model_config = ConfigDict(frozen=True)

    enterprise_name: str
    industry_type: str = Field(default="AI_NATIVE_SAAS")
    selected_capabilities: tuple[str, ...] = ()
    deployment_target: str = Field(default="CLOUD_CONTAINER")


class GeneratedEnterpriseOutput(BaseModel):
    """Entity representing generated enterprise artifacts manifest."""

    model_config = ConfigDict(frozen=True)

    generation_id: str
    enterprise_name: str
    generated_packages_count: int
    generated_specs_count: int
    is_constitution_compliant: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
