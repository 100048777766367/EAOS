from packages.evolution.application.use_cases import (
    ProposeEvolutionRequest,
    ProposeEvolutionUseCase,
)
from packages.evolution.domain.models import Evidence
from packages.evolution.infrastructure.adapters import InMemoryEvolutionRepository


def test_propose_evolution_lifecycle() -> None:
    repo = InMemoryEvolutionRepository()
    use_case = ProposeEvolutionUseCase(repo)

    # Đề xuất một trạng thái tiến hóa của AI Agent Coder
    request = ProposeEvolutionRequest(
        id="EVO-CODER-01",
        name="Coder Agent Config Profile",
        payload={"max_retry_loops": 10, "llm_fallback": "llama-3"},
        author="ArchitectAgent",
        triggered_by="Self optimization rule",
    )

    # Bằng chứng đo lường thực tế đạt tiêu chuẩn
    evidences = [
        Evidence(
            metric_name="Unit Test Coverage",
            metric_value=0.98,
            passed=True,
            log_summary="All core units passed successfully.",
        )
    ]

    result = use_case.execute(request, evidences)

    # Kiểm chứng các Invariants trong Domain và Application
    assert result.id == "EVO-CODER-01"
    assert result.metadata.environment == "production"
    assert result.provenance.author == "ArchitectAgent"
    assert len(result.evidences) == 1
    assert result.evidences[0].passed is True

    # Kiểm chứng khả năng lưu giữ của Repository
    saved_obj = repo.find_by_id("EVO-CODER-01")
    assert saved_obj is not None
    assert saved_obj.payload["max_retry_loops"] == 10