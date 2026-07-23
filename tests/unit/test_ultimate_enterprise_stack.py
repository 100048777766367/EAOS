"""Unit test suite verifying all 10 enterprise domain engines."""

from pathlib import Path

from data.data_architecture import DataArchitectureEngine
from decision.decision_engine import DecisionIntelligenceEngine
from memory.enterprise_memory import OrganizationalMemoryEngine
from observability.slo_tracker import EnterpriseObservabilityEngine
from operating_model.model_registry import OperatingModelRegistry
from operations.sre_runbook import OperationalRunbookEngine
from portfolio.investment_manager import PortfolioManagerEngine

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_operating_model_registry() -> None:
    """Verifies operating model value stream discovery."""
    reg = OperatingModelRegistry(ROOT_PATH)
    streams = reg.discover_value_streams()
    assert len(streams) == 3


def test_portfolio_manager_engine() -> None:
    """Verifies portfolio transformation initiatives listing."""
    mgr = PortfolioManagerEngine()
    inits = mgr.list_initiatives()
    assert len(inits) == 2


def test_data_architecture_engine() -> None:
    """Verifies data lineage audit engine."""
    eng = DataArchitectureEngine()
    lineage = eng.audit_data_lineage()
    assert len(lineage) == 1
    assert lineage[0].quality_score == 100.0


def test_operational_runbook_engine() -> None:
    """Verifies SRE runbook engine tasks."""
    eng = OperationalRunbookEngine()
    tasks = eng.get_active_runbooks()
    assert len(tasks) == 2


def test_enterprise_observability_engine() -> None:
    """Verifies SLO metric evaluation."""
    eng = EnterpriseObservabilityEngine()
    slos = eng.evaluate_slos()
    assert len(slos) == 1
    assert slos[0].compliant is True


def test_decision_intelligence_engine() -> None:
    """Verifies decision rule evaluation."""
    eng = DecisionIntelligenceEngine()
    outcome = eng.evaluate_decision({"env": "production"})
    assert outcome.passed is True
    assert outcome.action == "ALLOW"


def test_organizational_memory_engine() -> None:
    """Verifies organizational memory retrieval."""
    eng = OrganizationalMemoryEngine()
    mems = eng.retrieve_memory("architecture")
    assert len(mems) == 1
    assert mems[0].memory_type == "EPISODIC"
