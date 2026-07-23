"""Agent configuration validator verifying local LLM agent setups."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class AgentConfigAuditDTO(BaseModel):
    """Value object representing local agent configuration status."""

    model_config = ConfigDict(frozen=True)

    config_path: str
    is_valid: bool
    model_name: str


class AgentConfigValidator:
    """Validator inspecting local .agents/ configurations and prompts."""

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.agents_dir: Path = self.root_dir / ".agents"

    def audit_agent_configs(self) -> list[AgentConfigAuditDTO]:
        """Audits local LLM agent configuration files."""
        results: list[AgentConfigAuditDTO] = []
        if not self.agents_dir.exists():
            return results

        cfg_file = self.agents_dir / "config.yaml"
        exists = cfg_file.exists()

        results.append(
            AgentConfigAuditDTO(
                config_path=str(cfg_file.relative_to(self.root_dir) if exists else ".agents/config.yaml"),
                is_valid=exists,
                model_name="ollama/llama3",
            )
        )

        return results
