"""Integration unit test suite verifying all 7 architectural gap upgrades."""

from pathlib import Path

from engine.loader.capability_hot_loader import CapabilityHotLoader
from engine.validator.specification_validator import (
    SpecificationValidatorEngine,
)
from fitness.ai.hallucination_fitness import AIHallucinationFitness
from fitness.architecture.boundary_fitness import ArchitectureBoundaryFitness
from fitness.governance.constitution_fitness import (
    ConstitutionFitnessEvaluator,
)
from fitness.performance.latency_fitness import PerformanceLatencyFitness
from fitness.quality.coverage_fitness import CodeQualityCoverageFitness
from fitness.security.vulnerability_fitness import SecurityVulnerabilityFitness
from platform_services.ai.local_ollama_adapter import LocalOllamaAdapter
from tools.bootstrap.environment_initializer import (
    EnvironmentInitializerEngine,
)

ROOT_PATH = Path(__file__).resolve().parents[2]


def test_gap1_environment_initializer_engine() -> None:
    """Verifies Gap 1 environment bootstrapper directory and policy creation."""
    initializer = EnvironmentInitializerEngine(ROOT_PATH)
    res = initializer.initialize_environment()
    assert res.success is True
    assert isinstance(res.created_directories, list)


def test_gap2_concrete_6d_fitness_evaluators() -> None:
    """Verifies Gap 2 concrete 6D fitness evaluators suite."""
    arch_fit = ArchitectureBoundaryFitness().evaluate_boundaries(ROOT_PATH)
    assert arch_fit["dimension"] == "ARCHITECTURE"
    assert arch_fit["score"] >= 60.0

    gov_fit = ConstitutionFitnessEvaluator().evaluate_constitution(ROOT_PATH)
    assert gov_fit["dimension"] == "GOVERNANCE"

    sec_fit = SecurityVulnerabilityFitness().evaluate_security()
    assert sec_fit["score"] == 100.0

    perf_fit = PerformanceLatencyFitness().evaluate_latency()
    assert perf_fit["p99_latency_ms"] <= 50.0

    qual_fit = CodeQualityCoverageFitness().evaluate_quality()
    assert qual_fit["score"] == 100.0

    ai_fit = AIHallucinationFitness().evaluate_ai_drift()
    assert ai_fit["score"] == 100.0


def test_gap3_local_ollama_adapter_fallback() -> None:
    """Verifies Gap 3 local edge Ollama AI adapter offline resilience."""
    adapter = LocalOllamaAdapter()
    res = adapter.generate_completion("Summarize EAOS Constitution")
    assert res.offline_fallback is True
    assert "EAOS Local Edge AI Response" in res.content


def test_gap4_specification_validator_engine() -> None:
    """Verifies Gap 4 specification and schema validator engine."""
    val_engine = SpecificationValidatorEngine(ROOT_PATH)
    res = val_engine.validate_all_specifications()
    assert res.valid is True
    assert res.total_specs_found >= 1


def test_gap5_capability_hot_loader() -> None:
    """Verifies Gap 5 capability hot-plug dynamic importer."""
    loader = CapabilityHotLoader(ROOT_PATH)
    res = loader.hot_plug_capability("identity")
    assert res.loaded is True
    assert "identity" in res.capability_name
