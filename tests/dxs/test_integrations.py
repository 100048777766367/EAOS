from __future__ import annotations

from dxs.application.integration_service import IntegrationService


def test_integration_service_detects_github(tmp_path):
    (tmp_path / ".github").mkdir()

    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname='test'\n",
        encoding="utf-8",
    )

    result = IntegrationService().inspect(tmp_path)

    github = next(check for check in result.checks if check.name == ".github")

    assert github.exists is True


def test_integration_service_requires_pyproject(tmp_path):
    result = IntegrationService().inspect(tmp_path)

    pyproject = next(check for check in result.checks if check.name == "pyproject.toml")

    assert pyproject.exists is False
