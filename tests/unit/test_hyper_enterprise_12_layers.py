"""Unit test suite for 12 hyper-enterprise architectural layers."""

from pathlib import Path

from catalog.domain_element_catalog import DomainElementCatalog
from contexts.context_registry import BoundedContextRegistry
from platform_layer.platform_abstraction import (
    EnterprisePlatformRegistry,
)

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


def test_bounded_context_registry_discovers_all_6_contexts() -> None:
    """Verifies that context registry discovers all 6 bounded contexts."""
    registry = BoundedContextRegistry(ROOT_PATH)
    contexts = registry.discover_contexts()
    assert len(contexts) == 6
    names = [c.context_name for c in contexts]
    assert "sales" in names
    assert "crm" in names
    assert "erp" in names
    assert "finance" in names
    assert "marketing" in names
    assert "hr" in names


def test_domain_element_catalog_audits_5_categories() -> None:
    """Verifies domain element catalog audits all 5 categories."""
    catalog = DomainElementCatalog(ROOT_PATH)
    audits = catalog.audit_domain_catalog()
    assert len(audits) == 5
    types = [a.element_type for a in audits]
    assert "entities" in types
    assert "events" in types
    assert "commands" in types


def test_enterprise_platform_registry() -> None:
    """Verifies platform abstraction status registry."""
    reg = EnterprisePlatformRegistry()
    statuses = reg.get_platform_status()
    assert len(statuses) == 5
    assert all(s.is_active for s in statuses)
