"""Unit test suite for EAOS static schema validator engine."""

from pathlib import Path

from tools.schemas.schema_validator import SchemaValidatorEngine

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_schema_validator_validates_all_6_categories() -> None:
    """Verifies schema validator discovers and parses JSON schemas."""
    engine = SchemaValidatorEngine(ROOT_PATH)
    reports = engine.validate_all_schemas()
    assert len(reports) >= 6
    categories = {r.category for r in reports}
    assert "api" in categories
    assert "compiler" in categories
    assert "events" in categories
    assert "knowledge" in categories
    assert "representation" in categories
    assert "storage" in categories
    assert all(r.is_valid_json for r in reports)
