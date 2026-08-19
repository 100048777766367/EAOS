"""API Application Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    """Configuration settings for EAOS API Gateway."""

    model_config = SettingsConfigDict(env_prefix="EAOS_API_", env_file=".env", extra="ignore")
    title: str = "EAOS API Gateway"
    version: str = "0.1.0"
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False


GatewaySettings = APISettings
api_settings = APISettings()
