from pathlib import Path

from engine.compiler.architecture_compiler import ArchitectureCompiler
from tools.digital_twin.digital_twin import DigitalTwinOrchestrator
from tools.graph.dependency_graph_generator import DependencyGraphGenerator
from tools.time_machine.time_machine import ArchitectureTimeMachine
from tools.validate.architecture_validator import ArchitectureValidator


def test_master_architecture_tools_flow(tmp_path: Path) -> None:
    # 1. ARCHITECTURE VALIDATOR & NAMING CONVENTIONS
    validator = ArchitectureValidator(tmp_path)
    pkg_dir = tmp_path / "packages" / "mock_pkg"
    dom_dir = pkg_dir / "domain"
    infra_dir = pkg_dir / "infrastructure"
    dom_dir.mkdir(parents=True, exist_ok=True)
    infra_dir.mkdir(parents=True, exist_ok=True)

    # Thử chèn một vi phạm ranh giới
    domain_file = dom_dir / "models.py"
    domain_file.write_text("from packages.mock_pkg.infrastructure.adapters import CustomDb\n", encoding="utf-8")
    
    passed = validator.run_all_checks()
    assert passed is False
    assert any("Layer Violation" in v for v in validator.violations)

    # 2. DEPENDENCY GRAPH GENERATOR
    generator = DependencyGraphGenerator(tmp_path)
    assert generator.generate() is True
    assert (tmp_path / "generated" / "architecture" / "dependency_graph.json").exists()

    # 3. DIGITAL TWIN SIMULATION
    orchestrator = DigitalTwinOrchestrator(tmp_path)
    valid_proposal = {
        "package_name": "eaos-finance",
        "layer": "infrastructure",
        "dependencies": ["packages.knowledge.domain"],
    }
    res_valid = orchestrator.evaluate_proposal(valid_proposal)
    assert res_valid["status"] == "APPROVED"

    # 4. ARCHITECTURE TIME MACHINE snap v1 vs v2
    time_machine = ArchitectureTimeMachine(tmp_path)
    snap_v1 = time_machine.record_snapshot("v1")
    assert snap_v1["snapshot_id"] == "v1"

    # 5. ARCHITECTURE COMPILER
    compiler = ArchitectureCompiler(tmp_path)
    spec = {
        "capability_name": "billing",
        "description": "Billing Spec",
        "entities": [{"name": "Invoice", "fields": {"id": "str", "amount": "float"}}],
    }
    assert compiler.compile_spec(spec) is True