"""Environment configuration loader and settings schema for EAOS."""

import os
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict


class SystemEnvironment(StrEnum):
    """Enumeration of system runtime environments."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class DatabaseConfigDTO(BaseModel):
    """Value object representing database connection settings."""

    model_config = ConfigDict(frozen=True)

    url: str
    pool_size: int
    max_overflow: int


class RedisConfigDTO(BaseModel):
    """Value object representing Redis cache connection settings."""

    model_config = ConfigDict(frozen=True)

    url: str
    max_connections: int


class EnvironmentSettingsDTO(BaseModel):
    """Value object containing application environment settings."""

    model_config = ConfigDict(frozen=True)

    environment: SystemEnvironment
    debug: bool
    api_port: int
    database: DatabaseConfigDTO
    redis: RedisConfigDTO


class EnvironmentConfigLoader:
    """Loader reading environment-specific settings manifests."""

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.configs_dir: Path = self.root_dir / "configs"

    def load_settings(
        self,
        env_name: str | None = None,
    ) -> EnvironmentSettingsDTO:
        """Loads configuration settings for target environment."""
        raw_env = env_name or os.getenv("EAOS_ENV", "development")
        target_str = str(raw_env).lower()
        env_enum = SystemEnvironment.DEVELOPMENT

        for item in SystemEnvironment:
            if item.value == target_str:
                env_enum = item
                break

        yaml_path = self.configs_dir / env_enum.value / "settings.yaml"
        data = self._read_simple_yaml(yaml_path)

        db_data = data.get("database", {})
        redis_data = data.get("redis", {})

        is_prod = env_enum == SystemEnvironment.PRODUCTION
        default_db = (
            "postgresql://eaos:eaos_secure_pass_2026@localhost:5432/eaos_db"
            if is_prod
            else "postgresql://eaos:eaos@localhost:5432/eaos"
        )

        return EnvironmentSettingsDTO(
            environment=env_enum,
            debug=bool(data.get("debug", not is_prod)),
            api_port=int(data.get("api_port", 8000)),
            database=DatabaseConfigDTO(
                url=os.getenv("DATABASE_URL", str(db_data.get("url", default_db))),
                pool_size=int(db_data.get("pool_size", 10)),
                max_overflow=int(db_data.get("max_overflow", 20)),
            ),
            redis=RedisConfigDTO(
                url=os.getenv(
                    "REDIS_URL",
                    str(redis_data.get("url", "redis://localhost:6379/0")),
                ),
                max_connections=int(redis_data.get("max_connections", 50)),
            ),
        )

    def _read_simple_yaml(self, path: Path) -> dict[str, Any]:
        """Simple line parser for flat settings.yaml configs."""
        if not path.exists():
            return {}

        result: dict[str, Any] = {}
        current_section = ""

        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            if line.endswith(":") and not line.startswith(" "):
                current_section = line.rstrip(":").strip()
                result[current_section] = {}
            elif ":" in stripped:
                parts = stripped.split(":", 1)
                key = parts[0].strip()
                val = parts[1].strip().strip('"').strip("'")

                typed_val: Any = val
                if val.lower() == "true":
                    typed_val = True
                elif val.lower() == "false":
                    typed_val = False
                elif val.isdigit():
                    typed_val = int(val)

                if current_section and isinstance(result.get(current_section), dict):
                    result[current_section][key] = typed_val
                else:
                    result[key] = typed_val

        return result
