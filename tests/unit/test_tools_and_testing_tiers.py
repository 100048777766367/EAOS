"""Unit test suite for EAOS internal architectural tools."""

from pathlib import Path

from tools.benchmark.load_tester import SystemLoadBenchmarkTool
from tools.doctor.main import MonorepoDoctorTool
from tools.generator.code_synthesizer import BoilerplateGeneratorTool
from tools.migrate.migration_manager import DatabaseMigrationManager

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_system_load_benchmark_tool() -> None:
    """Verifies load tester benchmark SLA evaluation."""
    tool = SystemLoadBenchmarkTool()
    res = tool.run_benchmark("/health", requests=100)
    assert res.sla_passed is True
    assert res.p99_latency_ms <= 50.0


def test_monorepo_doctor_diagnoses_health() -> None:
    """Verifies monorepo doctor health score report."""
    doctor = MonorepoDoctorTool(ROOT_PATH)
    report = doctor.diagnose_system()
    assert report.overall_health_score == 100
    assert report.ast_compliant is True


def test_boilerplate_generator_scaffolding() -> None:
    """Verifies code synthesizer package scaffolding."""
    gen = BoilerplateGeneratorTool(ROOT_PATH)
    res = gen.generate_package("analytics")
    assert res.status == "GENERATED"
    assert len(res.created_files) == 3


def test_database_migration_manager() -> None:
    """Verifies schema migration manager execution status."""
    mgr = DatabaseMigrationManager(ROOT_PATH)
    status = mgr.apply_migrations()
    assert status.status == "MIGRATIONS_APPLIED"
    assert status.vector_extension_active is True
