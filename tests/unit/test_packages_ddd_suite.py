"""Unit test suite verifying all packages DDD bounded context layers."""

from packages.analytics.application.use_cases import (
    ComputeSystemHealthUseCase,
)
from packages.analytics.infrastructure.adapters import (
    InMemoryAnalyticsRepository,
)
from packages.shared.domain.models import EntityIdVO


def test_packages_ddd_layering_execution() -> None:
    """Verifies analytics package domain, application, and infrastructure."""
    use_case = ComputeSystemHealthUseCase()
    entity = use_case.execute(system_id="SYS-001", metric_value=18.4)

    assert entity.system_id == "SYS-001"
    assert len(entity.trends) == 1
    assert entity.trends[0].value == 18.4

    repo = InMemoryAnalyticsRepository()
    saved = repo.save(entity)
    assert saved.metric_id == entity.metric_id

    fetched = repo.find_by_system_id("SYS-001")
    assert fetched is not None
    assert fetched.system_id == "SYS-001"


def test_shared_kernel_entity_id_vo() -> None:
    """Verifies shared kernel entity ID value object."""
    entity_id = EntityIdVO(id_value="ID-SHARED-100")
    assert entity_id.id_value == "ID-SHARED-100"
