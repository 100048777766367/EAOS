from apps.cli.main import app
from typer.testing import CliRunner

runner = CliRunner()

def test_version_command() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "EAOS CLI" in result.output

def test_info_command() -> None:
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "Enterprise Architecture Operating System" in result.output