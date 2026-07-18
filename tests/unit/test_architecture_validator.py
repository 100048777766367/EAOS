from pathlib import Path

from tools.validate.architecture_validator import ArchitectureValidator


def test_production_codebase_compliance() -> None:
    """Kiểm chứng codebase thực tế của EAOS tuân thủ 100% Hiến pháp."""
    root_dir = Path(__file__).resolve().parent.parent.parent
    validator = ArchitectureValidator(root_dir)

    passed = validator.run_all_checks()
    # Toàn bộ mã nguồn thật hiện có bắt buộc phải xanh mướt
    assert passed is True
    assert len(validator.violations) == 0


def test_mock_architecture_violations(tmp_path: Path) -> None:
    """Mô phỏng vi phạm ranh giới và kiểm chứng validator phát hiện chính xác."""
    # Tạo cấu trúc package giả lập có vi phạm
    pkg_dir = tmp_path / "packages" / "mock_pkg"
    dom_dir = pkg_dir / "domain"
    infra_dir = pkg_dir / "infrastructure"

    dom_dir.mkdir(parents=True)
    infra_dir.mkdir(parents=True)

    # Vi phạm 1: Tầng domain import trái phép từ infrastructure
    domain_file = dom_dir / "models.py"
    domain_file.write_text(
        "from packages.mock_pkg.infrastructure.adapters import CustomDb\n",
        encoding="utf-8",
    )

    # Vi phạm 2: Định danh sai quy tắc UseCase trong application
    app_dir = pkg_dir / "application"
    app_dir.mkdir(parents=True)
    use_case_file = app_dir / "use_cases.py"
    use_case_file.write_text("class SloppyClass:\n    pass\n", encoding="utf-8")

    validator = ArchitectureValidator(tmp_path)
    passed = validator.run_all_checks()

    assert passed is False
    assert len(validator.violations) == 2
    # Sửa lỗi: Sử dụng any() để kiểm tra không quan trọng thứ tự xuất hiện
    assert any("Layer Violation" in v for v in validator.violations)
    assert any("Naming Violation" in v for v in validator.violations)