"""Settings for the EAOS AIDE application boundary."""

from functools import lru_cache

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AideSettings(BaseSettings):
    """Runtime configuration for AIDE as an engineering client."""

    model_config = SettingsConfigDict(env_prefix="AIDE_")

    title: str = "EAOS AIDE"
    version: str = "0.1.0"
    host: str = "127.0.0.1"
    port: int = 6932
    api_base_url: AnyHttpUrl = Field(
        default="http://127.0.0.1:8000",
        description="Enterprise Engineering Gateway base URL.",
    )
    api_ws_url: str = "ws://127.0.0.1:8000/ws/chat"
    web_url: AnyHttpUrl = "http://127.0.0.1:3002"
    github_url: AnyHttpUrl = "https://github.com"


@lru_cache
def get_settings() -> AideSettings:
    """Return cached AIDE settings."""

    return AideSettings()
