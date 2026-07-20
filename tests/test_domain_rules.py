from pathlib import Path
from libs.validation.checker import ASTBoundaryChecker, parse_adr_file

def test_ast_boundary_checking():
    """Đảm bảo nhân quét AST hoạt động chính xác."""
    root_dir = Path(__file__).resolve().parent.parent
    checker = ASTBoundaryChecker(root_dir)
    graph = checker.scan_dependencies()
    assert isinstance(graph, dict)

def test_adr_structure_parsing(tmp_path):
    """Đảm bảo bóc tách cấu trúc tệp tin ADRs đạt chuẩn."""
    adr_file = tmp_path / "ADR-001.md"
    adr_file.write_text(
        "# ADR-001 Hexagonal Architecture\n## Status\nStatus: Accepted\n## Context\nAdopt.\n## Decision\nYes.\n## Consequences\nDone.",
        encoding="utf-8"
    )
    doc = parse_adr_file(adr_file)
    assert doc.title == "ADR-001 Hexagonal Architecture"
    assert doc.status == "Accepted"
    assert doc.has_consequences_header is True
