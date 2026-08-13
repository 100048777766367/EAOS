from pathlib import Path

from dxs.doctor.service import run_doctor


def test_doctor_writes_evidence(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname='test'\n",
        encoding="utf-8",
    )
    evidence, evidence_path = run_doctor(tmp_path)
    assert evidence.status == "passed"
    assert evidence_path.exists()
