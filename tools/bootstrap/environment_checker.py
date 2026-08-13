import shutil

from pydantic import BaseModel, ConfigDict

"""Laptop Environment Readiness Checker for EAOS Local Deployment."""


class EnvironmentCheckDTO(BaseModel):
    """Value object representing local laptop tool readiness."""

    model_config = ConfigDict(frozen=True)

    tool_name: str
    is_installed: bool
    recommendation: str


class LaptopEnvironmentChecker:
    """Checker inspecting presence of required open-source software."""

    REQUIRED_TOOLS: tuple[str, ...] = (
        "git",
        "python",
        "uv",
        "docker",
        "ollama",
    )

    def check_tools(self) -> list[EnvironmentCheckDTO]:
        """Audits presence of local CLI binaries."""
        results: list[EnvironmentCheckDTO] = []
        for tool in self.REQUIRED_TOOLS:
            found = shutil.which(tool) is not None
            rec = "INSTALLED & READY" if found else f"Please install {tool}"
            results.append(
                EnvironmentCheckDTO(
                    tool_name=tool,
                    is_installed=found,
                    recommendation=rec,
                )
            )
        return results


if __name__ == "__main__":
    checker = LaptopEnvironmentChecker()
    checks = checker.check_tools()
    print("====================================================")
    print(" EAOS LAPTOP ENVIRONMENT READINESS AUDIT            ")
    print("====================================================")
    for c in checks:
        status_icon = "✔" if c.is_installed else "✖"
        print(f"{status_icon} {c.tool_name:<10} : {c.recommendation}")
    print("====================================================")
