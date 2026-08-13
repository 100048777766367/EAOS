from __future__ import annotations

from dxs.application.ide_service import IdeService


def test_ide_service_detects_vscode(tmp_path):
    (tmp_path / ".vscode").mkdir()

    result = IdeService().inspect(tmp_path)

    vscode = next(check for check in result.checks if check.name == ".vscode")

    assert vscode.exists is True


def test_ide_service_detects_missing_ide(tmp_path):
    result = IdeService().inspect(tmp_path)

    assert result.passed is False
