"""Unit test suite for EAOS agent configuration validator."""

from pathlib import Path

from tools.agents.agent_config_validator import AgentConfigValidator

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_agent_config_validator_audits_config() -> None:
    """Verifies that agent config validator audits .agents/config.yaml."""
    validator = AgentConfigValidator(ROOT_PATH)
    audits = validator.audit_agent_configs()
    assert len(audits) == 1
    assert audits[0].is_valid is True
    assert audits[0].model_name == "ollama/llama3"
