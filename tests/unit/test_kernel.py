import pytest
from kernel.runtime.main import boot


def test_kernel_boot(capsys: pytest.CaptureFixture[str]) -> None:
    boot()
    captured = capsys.readouterr()
    assert "EAOS Kernel Booted Successfully." in captured.out