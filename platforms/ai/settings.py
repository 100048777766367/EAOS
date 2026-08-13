"""EAOS Environment Settings Manager using Pydantic v2."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EAOSSettings(BaseSettings):
    """Configuration Settings mapped strictly from .env file."""

    app_name: str = Field(default="EAOS API Gateway", alias="APP_NAME")
    environment: str = Field(default="production", alias="ENVIRONMENT")
    database_url: str = Field(
        default="postgresql://eaos:eaos@localhost:5433/eaos",
        alias="DATABASE_URL",
    )

    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="nemotron-mini", alias="OLLAMA_MODEL")
    default_ai_provider: str = Field(default="gemini", alias="DEFAULT_AI_PROVIDER")

    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-flash-latest", alias="GEMINI_MODEL")
    gemini_api_keys: str = Field(default="", alias="GEMINI_API_KEYS")

    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    huggingface_api_key: str = Field(default="", alias="HUGGINGFACE_API_KEY")
    cohere_api_key: str = Field(default="", alias="COHERE_API_KEY")

    enable_feature_x: bool = Field(default=True, alias="ENABLE_FEATURE_X")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


eaos_settings = EAOSSettings()
