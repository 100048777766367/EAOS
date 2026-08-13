from pydantic import BaseModel, ConfigDict, Field

"""Production Cloud & Public Domain Deployment Adapter for EAOS."""


class CloudDeploymentConfigDTO(BaseModel):
    """Value object representing public production cloud settings."""

    model_config = ConfigDict(frozen=True)

    public_domain: str = Field(default="api.eaos.ai")
    cloud_database_url: str = Field(..., description="Public Managed DB")
    ssl_enabled: bool = True
    cloudflare_tunnel_active: bool = True
    stripe_webhook_live: bool = True


class ProductionCloudDeploymentEngine:
    """Engine managing transition from localhost to public cloud."""

    def evaluate_production_readiness(self, config: CloudDeploymentConfigDTO) -> bool:
        """Verifies that database and domain are no longer localhost."""
        is_local_db = "localhost" in config.cloud_database_url
        is_local_domain = "localhost" in config.public_domain
        return not (is_local_db or is_local_domain)


if __name__ == "__main__":
    engine = ProductionCloudDeploymentEngine()
    prod_cfg = CloudDeploymentConfigDTO(
        public_domain="api.eaos.ai",
        cloud_database_url="postgresql://eaos:sec@db.hetzner.com:5432/eaos",
    )
    is_ready = engine.evaluate_production_readiness(prod_cfg)
    print(f"✔ Production Cloud Readiness Verified: {is_ready}")
