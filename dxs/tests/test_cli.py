from __future__ import annotations

import subprocess
import sys


def test_cli_module_imports() -> None:
    result = subprocess.run(
        [sys.executable, "-c", "import dxs.cli.main"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_cli_help() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "dxs.cli.main", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "EAOS Developer Experience System" in result.stdout
    assert "doctor" in result.stdout
    assert "discover" in result.stdout
    assert "validate" in result.stdout
    assert "diagnose" in result.stdout
    assert "health" in result.stdout
    assert "evidence" in result.stdout
    assert "compatibility" in result.stdout
    assert "migration" in result.stdout
    assert "evolution" in result.stdout
    assert "remediation" in result.stdout
    assert "scaffold" in result.stdout
    assert "workspace" in result.stdout
    assert "documentation" in result.stdout
    assert "ide" in result.stdout
    assert "integrations" in result.stdout
    assert "ai" in result.stdout
    assert "policies" in result.stdout
    assert "governance" in result.stdout
    assert "orchestration" in result.stdout
    assert "observability" in result.stdout
    assert "self-diagnostics" in result.stdout


def test_ai_subcommand_help() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "dxs.cli.main", "ai", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "capability" in result.stdout
    assert "policy" in result.stdout
    assert "adapter" in result.stdout
