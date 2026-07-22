"""Unit tests for Architecture Fitness Engine and Graph Analysis."""

from packages.architecture_fitness.application.dto import (
    EvaluateFitnessSuiteCommand,
    EvaluationItemDTO,
)
from packages.architecture_fitness.application.use_cases import (
    EvaluateFitnessSuiteUseCase,
    QueryADRIncidentImpactUseCase,
)
from packages.architecture_fitness.domain.models import FitnessDimension
from packages.architecture_fitness.infrastructure.adapters import (
    InMemoryFitnessRepository,
)


def test_fitness_suite_evaluation_and_adr_incident_query() -> None:
    repo = InMemoryFitnessRepository()
    eval_uc = EvaluateFitnessSuiteUseCase(repo)
    query_uc = QueryADRIncidentImpactUseCase(repo)

    # 1. Record Evaluation linked to ADR-001 (No Incident)
    eval_uc.execute(
        EvaluateFitnessSuiteCommand(
            suite_id="SUITE-01",
            business_goal_id="GOAL-STABILITY",
            capability_id="CAP-IDENTITY",
            adr_id="ADR-001",
            rule_id="RULE-R4",
            commit_hash="c111111",
            author_id="ArchitectAgent",
            incident_id=None,
            evaluations=[
                EvaluationItemDTO(
                    dimension=FitnessDimension.LAYER_BOUNDARY,
                    rule_id="RULE-R4",
                    passed=True,
                    score=1.0,
                    evidence_details="Clean hexagonal layer boundaries.",
                )
            ],
        )
    )

    # 2. Record 2 Evaluations linked to ADR-002 (With Incidents INC-101, INC-102)
    eval_uc.execute(
        EvaluateFitnessSuiteCommand(
            suite_id="SUITE-02",
            business_goal_id="GOAL-PERFORMANCE",
            capability_id="CAP-KNOWLEDGE",
            adr_id="ADR-002",
            rule_id="RULE-R15",
            commit_hash="c222222",
            author_id="CoderAgent",
            incident_id="INC-101-OOM-RAM",
            evaluations=[
                EvaluationItemDTO(
                    dimension=FitnessDimension.DOMAIN_PURITY,
                    rule_id="RULE-R15",
                    passed=False,
                    score=0.2,
                    evidence_details="Unbounded RAM growth.",
                )
            ],
        )
    )

    eval_uc.execute(
        EvaluateFitnessSuiteCommand(
            suite_id="SUITE-03",
            business_goal_id="GOAL-PERFORMANCE",
            capability_id="CAP-KNOWLEDGE",
            adr_id="ADR-002",
            rule_id="RULE-R15",
            commit_hash="c333333",
            author_id="CoderAgent",
            incident_id="INC-102-TIMEOUT",
            evaluations=[
                EvaluationItemDTO(
                    dimension=FitnessDimension.SECURITY_GUARD,
                    rule_id="RULE-R15",
                    passed=False,
                    score=0.4,
                    evidence_details="Slow query timeout.",
                )
            ],
        )
    )

    # 3. Query: "ADR nào gây nhiều incident nhất?"
    impact_report = query_uc.execute()

    assert len(impact_report) == 1
    top_adr = impact_report[0]
    assert top_adr.adr_id == "ADR-002"
    assert top_adr.incident_count == 2
    assert top_adr.rank == 1
