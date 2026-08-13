from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

"""Web Application Settings."""


class WebSettings(BaseSettings):
    """Configuration settings for EAOS Web UI Gateway."""

    model_config = SettingsConfigDict(
        env_prefix="EAOS_WEB_",
        env_file=".env",
        extra="ignore",
    )

    title: str = Field(default="EAOS Web UI Gateway")
    version: str = Field(default="0.2.0")
    debug: bool = Field(default=False)
    api_gateway_url: str = Field(default="http://localhost:8000")
    host: str = Field(
        default="127.0.0.1",
        description="Host interface binding for local web UI",
    )
    port: int = Field(default=3002)
    secret_key: str = Field(default="web-secret-key-change-in-prod")


web_settings = WebSettings()
