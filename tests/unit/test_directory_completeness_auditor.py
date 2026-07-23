"""Unit tests for DirectoryCompletenessAuditor and conflict analysis engine."""

from pathlib import Path

from tools.audit.directory_completeness_auditor import (
    AuditReport,
    DirectoryCompletenessAuditor,
    DirectoryConflict,
)

ROOT_PATH = Path(".")


def test_directory_completeness_auditor_analyzes_conflicts() -> None:
    """Verifies conflict analysis engine strategy recommendations."""
    auditor = DirectoryCompletenessAuditor(ROOT_PATH)
    conflicts = auditor.analyze_splitting_conflicts()
    assert isinstance(conflicts, list)
    for conflict in conflicts:
        assert isinstance(conflict, DirectoryConflict)
        assert hasattr(conflict, "recommended_strategy")
        assert hasattr(conflict, "conflict_type")


def test_clean_directory_structure(tmp_path: Path) -> None:
    """Verify clean directory structure with active files passes audit."""
    pkg_dir = tmp_path / "packages" / "core"
    pkg_dir.mkdir(parents=True)
    (tmp_path / "packages" / "__init__.py").write_text("# Packages root")
    (pkg_dir / "__init__.py").write_text("# Core package")

    auditor = DirectoryCompletenessAuditor(root_path=tmp_path)
    report: AuditReport = auditor.execute_audit()

    assert report.is_clean
    assert report.completely_empty_count == 0
    assert report.hollow_count == 0
    assert len(report.conflicts) == 0


def test_unindexed_split_conflict_detection(tmp_path: Path) -> None:
    """Verify detection of unindexed split package hierarchy."""
    parent = tmp_path / "domain"
    child = parent / "subdomain"
    child.mkdir(parents=True)
    (child / "service.py").write_text("# Service code")

    # Parent intentionally lacks __init__.py
    auditor = DirectoryCompletenessAuditor(root_path=tmp_path)
    conflicts = auditor.analyze_splitting_conflicts()

    assert len(conflicts) == 1
    assert conflicts[0].conflict_type == "UNINDEXED_PACKAGE_SPLIT"
    assert conflicts[0].recommended_strategy == "ADD_PACKAGE_INDEX"
