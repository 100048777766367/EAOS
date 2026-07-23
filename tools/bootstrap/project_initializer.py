"""Project bootstrap initializer establishing EAOS workspace structure."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class BootstrapStatusDTO(BaseModel):
    """Value object representing workspace bootstrap initialization result."""

    model_config = ConfigDict(frozen=True)

    workspace_root: str
    initialized_directories: int
    status: str


class ProjectBootstrapTool:
    """Tool initializing monorepo directory skeleton and Git hooks."""

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()

    def initialize_workspace(self) -> BootstrapStatusDTO:
        """Ensures mandatory top-level directories exist."""
        top_dirs = (
            "apps",
            "packages",
            "kernel",
            "platform_services",
            "engine",
            "tools",
            "tests",
            "infra",
        )
        count = 0
        for d in top_dirs:
            p = self.root_dir / d
            if not p.exists():
                p.mkdir(parents=True, exist_ok=True)
            count += 1

        return BootstrapStatusDTO(
            workspace_root=str(self.root_dir),
            initialized_directories=count,
            status="BOOTSTRAPPED",
        )
