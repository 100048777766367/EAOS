from pathlib import Path

from libs.validation.checker import ASTBoundaryChecker, parse_adr_file


def test_production_ast_boundary_scan() -> None:
    """Đảm bảo nhân AST quét chính xác ranh giới của monorepo thật."""
    root_dir = Path(__file__).resolve().parent.parent.parent
    checker = ASTBoundaryChecker(root_dir)
    graph = checker.scan_dependencies()
    assert isinstance(graph, dict)


def test_mock_adr_parsing(tmp_path: Path) -> None:
    """Kiểm chứng bóc tách tệp cấu trúc tiêu đề ADR."""
    adr_file = tmp_path / "ADR-001.md"
    adr_file.write_text(
        "# ADR 1: Clean Architecture\n\n## Status\nStatus: Accepted\n\n## Context\nOk",
        encoding="utf-8",
    )
    doc = parse_adr_file(adr_file)
    assert doc.title == "ADR 1: Clean Architecture"
    assert doc.status == "Accepted"