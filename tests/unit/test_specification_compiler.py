"""Unit test suite for EAOS executable specification compiler."""

from pathlib import Path

from tools.specifications.specification_compiler import (
    SpecificationCompilerEngine,
)

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_specification_compiler_compiles_all_6_categories() -> None:
    """Verifies specification compiler compiles files across 6 categories."""
    engine = SpecificationCompilerEngine(ROOT_PATH)
    audits = engine.compile_all_specifications()
    assert len(audits) >= 6
    categories = {a.category for a in audits}
    assert "apis" in categories
    assert "business" in categories
    assert "capabilities" in categories
    assert "domains" in categories
    assert "services" in categories
    assert "workflows" in categories
    assert all(a.is_compiled for a in audits)
