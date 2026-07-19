from pathlib import Path

import pytest
from apps.cli.main import app
from kernel.governance.loop_engine import GovernanceLoopEngine, LoopTrigger
from kernel.runtime.main import boot
from typer.testing import CliRunner

runner = CliRunner()


def test_kernel_boot(capsys: pytest.CaptureFixture[str]) -> None:
    boot()
    captured = capsys.readouterr()
    assert "EAOS Kernel Booted Successfully." in captured.out


def test_cli_version_and_info() -> None:
    result_v = runner.invoke(app, ["version"])
    assert result_v.exit_code == 0
    assert "EAOS CLI" in result_v.output

    result_i = runner.invoke(app, ["info"])
    assert result_i.exit_code == 0
    assert "Enterprise Architecture" in result_i.output


def test_governance_loop_evaluation(tmp_path: Path) -> None:
    engine = GovernanceLoopEngine(tmp_path)
    docs_dir = tmp_path / "docs"

    trigger_exec = LoopTrigger(
        loop_type="EXECUTION", cadence="FAST", trigger_context="Unit testing"
    )

    # Thất bại khi thiếu TASK.md
    res_fail = engine.evaluate_loop(trigger_exec)
    assert res_fail.status == "FAILED"

    # Thành công khi tạo TASK.md
    task_file = docs_dir / "TASK.md"
    task_file.parent.mkdir(parents=True, exist_ok=True)
    task_file.write_text("- [ ] Implement feature\n", encoding="utf-8")
    res_pass = engine.evaluate_loop(trigger_exec)
    assert res_pass.status == "COMPLETED"

    # Vòng phản hồi Tiến hóa kiến trúc (Architecture Loop)
    trigger_arch = LoopTrigger(
        loop_type="ARCHITECTURE",
        cadence="MEDIUM",
        trigger_context="Unit testing",
    )
    res_arch_fail = engine.evaluate_loop(trigger_arch)
    assert res_arch_fail.status == "FAILED"

    # Bổ sung đầy đủ để thông qua gác cổng
    const_file = docs_dir / "ARCHITECTURE_CONSTITUTION.md"
    const_file.write_text("# Constitution\n", encoding="utf-8")

    meta_file = docs_dir / "architecture" / "EAOS_META_ARCHITECTURE.md"
    meta_file.parent.mkdir(parents=True, exist_ok=True)
    meta_file.write_text("# Meta Architecture\n", encoding="utf-8")

    adr_file = docs_dir / "decisions" / "ADR-001.md"
    adr_file.parent.mkdir(parents=True, exist_ok=True)
    adr_file.write_text("# ADR 001\n", encoding="utf-8")

    res_arch_pass = engine.evaluate_loop(trigger_arch)
    assert res_arch_pass.status == "COMPLETED"