"""Use cases for Architecture Fitness evaluation and ADR impact analysis."""

from packages.architecture_fitness.application.dto import (
    ADRIncidentImpactResponse,
    EvaluateFitnessSuiteCommand,
)
from packages.architecture_fitness.domain.models import (
    FitnessEvaluationResult,
    FitnessSuiteAggregate,
    KnowledgeGraphLink,
)
from packages.architecture_fitness.domain.ports import (
    FitnessRepositoryPort,
    GraphTraceabilityQueryPort,
)


class EvaluateFitnessSuiteUseCase:
    def __init__(self, repository: FitnessRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: EvaluateFitnessSuiteCommand) -> float:
        link = KnowledgeGraphLink(
            business_goal_id=command.business_goal_id,
            capability_id=command.capability_id,
            adr_id=command.adr_id,
            rule_id=command.rule_id,
            commit_hash=command.commit_hash,
            author_id=command.author_id,
            incident_id=command.incident_id,
        )

        suite = FitnessSuiteAggregate(suite_id=command.suite_id, graph_link=link)

        for item in command.evaluations:
            suite.add_evaluation(
                FitnessEvaluationResult(
                    dimension=item.dimension,
                    rule_id=item.rule_id,
                    passed=item.passed,
                    score=item.score,
                    evidence_details=item.evidence_details,
                )
            )

        self._repository.save(suite)
        return suite.overall_fitness_score


class QueryADRIncidentImpactUseCase:
    """Answers: 'ADR nào gây ra nhiều incident nhất?'"""

    def __init__(self, graph_query: GraphTraceabilityQueryPort) -> None:
        self._graph_query = graph_query

    def execute(self) -> list[ADRIncidentImpactResponse]:
        raw_results = self._graph_query.find_most_incident_prone_adrs()

        return [
            ADRIncidentImpactResponse(adr_id=adr_id, incident_count=count, rank=index + 1)
            for index, (adr_id, count) in enumerate(raw_results)
        ]
