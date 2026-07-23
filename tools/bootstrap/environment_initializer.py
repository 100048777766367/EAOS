"""EAOS environment bootstrap initializer engine."""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict

ROOT_PATH = Path(__file__).resolve().parents[2]


class BootstrapResultDTO(BaseModel):
    """Result data transfer object for environment bootstrap."""

    model_config = ConfigDict(frozen=True)

    success: bool
    created_directories: list[str]
    seeded_files: list[str]
    message: str


class EnvironmentInitializerEngine:
    """Engine for initializing runtime directories and seed configs."""

    REQUIRED_DIRS: tuple[str, ...] = (
        "runtime/cache",
        "runtime/events",
        "runtime/logs",
        "runtime/metrics",
        "runtime/policies",
        "runtime/registry",
        "runtime/sessions",
        "runtime/state",
        "runtime/traces",
        "data/postgres",
        "data/redis",
        "data/minio",
    )

    def __init__(self, root_path: Path | None = None) -> None:
        self.root_path: Path = root_path or ROOT_PATH

    def initialize_environment(self) -> BootstrapResultDTO:
        """Ensures all required runtime directories and seed files exist."""
        created_dirs: list[str] = []
        seeded_files: list[str] = []

        for rel_dir in self.REQUIRED_DIRS:
            target_dir = self.root_path / rel_dir
            if not target_dir.exists():
                target_dir.mkdir(parents=True, exist_ok=True)
                created_dirs.append(rel_dir)

        policy_path = self.root_path / "runtime" / "policies" / "active_runtime_policies.json"
        if not policy_path.exists():
            policy_data = {
                "version": "1.0.0",
                "rules": ["R01_DOMAIN_ISOLATION", "R13_CONSTITUTIONAL_GATE"],
                "active": True,
            }
            policy_path.write_text(json.dumps(policy_data, indent=2), encoding="utf-8")
            seeded_files.append("runtime/policies/active_runtime_policies.json")

        return BootstrapResultDTO(
            success=True,
            created_directories=created_dirs,
            seeded_files=seeded_files,
            message="Environment successfully bootstrapped and seeded.",
        )


def main() -> None:
    """CLI entrypoint for environment bootstrapper."""
    engine = EnvironmentInitializerEngine()
    res = engine.initialize_environment()
    print(f"[✔] {res.message}")


if __name__ == "__main__":
    main()
