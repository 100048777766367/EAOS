import shutil
from pathlib import Path

from pydantic import BaseModel, ConfigDict

"""Development Platform Orchestrator for Laptop Environment Setup."""


class DevToolStatusDTO(BaseModel):
    """Value object representing status of a development platform tool."""

    model_config = ConfigDict(frozen=True)

    tool_name: str
    category: str
    is_installed: bool
    resolved_path: str | None = None


class LaptopDevPlatformReportDTO(BaseModel):
    """Value object representing total laptop development environment status."""

    model_config = ConfigDict(frozen=True)

    is_env_ready: bool
    installed_tools_count: int
    total_required_tools: int
    tools_status: list[DevToolStatusDTO]


class LaptopDevPlatformOrchestrator:
    """Orchestrates and audits local laptop development platform tools."""

    REQUIRED_DEV_TOOLS: tuple[tuple[str, str], ...] = (
        ("git", "Version Control"),
        ("python", "Runtime Environment"),
        ("uv", "Package & Task Manager"),
        ("docker", "Container Runtime"),
        ("ollama", "Local AI Inference Engine"),
    )

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()

    def audit_dev_platform(self) -> LaptopDevPlatformReportDTO:
        """Inspects local system binaries for dev platform readiness."""
        statuses: list[DevToolStatusDTO] = []
        installed = 0

        for tool_bin, cat in self.REQUIRED_DEV_TOOLS:
            bin_path = shutil.which(tool_bin)
            found = bin_path is not None
            if found:
                installed += 1
            statuses.append(
                DevToolStatusDTO(
                    tool_name=tool_bin,
                    category=cat,
                    is_installed=found,
                    resolved_path=bin_path,
                )
            )

        total = len(self.REQUIRED_DEV_TOOLS)
        ready = installed == total

        return LaptopDevPlatformReportDTO(
            is_env_ready=ready,
            installed_tools_count=installed,
            total_required_tools=total,
            tools_status=statuses,
        )


if __name__ == "__main__":
    orch = LaptopDevPlatformOrchestrator()
    report = orch.audit_dev_platform()
    print("====================================================")
    print(" EAOS LAPTOP DEVELOPMENT PLATFORM AUDIT REPORT      ")
    print("====================================================")
    print(f"✔ Environment Ready : {report.is_env_ready}")
    print(f"✔ Tools Installed   : {report.installed_tools_count}/{report.total_required_tools}")
    print("====================================================")
