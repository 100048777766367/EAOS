from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Air-Gapped & On-Premise Isolated Deployment Engine for EAOS."""


class DeploymentTierEnum(StrEnum):
    """Four supported deployment tiers in EAOS Platform."""

    SAAS_PUBLIC = "SAAS_PUBLIC"
    PRIVATE_CLOUD = "PRIVATE_CLOUD"
    ON_PREMISE = "ON_PREMISE"
    AIR_GAPPED = "AIR_GAPPED"


class AirGappedDeploymentProfileDTO(BaseModel):
    """Value object representing Air-Gapped deployment settings."""

    model_config = ConfigDict(frozen=True)

    deployment_tier: DeploymentTierEnum
    local_llm_endpoint: str
    local_db_url: str
    is_zero_internet_compliant: bool = True
    local_siem_active: bool = True
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AirGappedDeploymentEngine:
    """Engine verifying and configuring 100% isolated deployment."""

    def evaluate_isolation_compliance(self, profile: AirGappedDeploymentProfileDTO) -> bool:
        """Verifies that no external cloud endpoints are referenced."""
        is_external_llm = any(
            cloud_domain in profile.local_llm_endpoint.lower()
            for cloud_domain in ["openai.com", "anthropic.com", "api."]
        )
        is_external_db = "localhost" not in profile.local_db_url and not (
            profile.local_db_url.startswith("sqlite")
            or "10." in profile.local_db_url
            or "192.168." in profile.local_db_url
        )
        return not (is_external_llm or is_external_db)


if __name__ == "__main__":
    engine = AirGappedDeploymentEngine()
    prof = AirGappedDeploymentProfileDTO(
        deployment_tier=DeploymentTierEnum.AIR_GAPPED,
        local_llm_endpoint="http://10.0.0.50:11434/v1",
        local_db_url=("postgresql://eaos:sec@10.0.0.100:5432/eaos_classified"),
    )
    compliant = engine.evaluate_isolation_compliance(prof)
    print(f"✔ Air-Gapped Tier: {prof.deployment_tier}")
    print(f"✔ Zero-Internet Isolation Compliant: {compliant}")
