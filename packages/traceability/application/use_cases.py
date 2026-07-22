"""Application use cases for Traceability query and registration."""

from packages.traceability.application.dto import (
    CodeChangeExplanationResponse,
    ExplainCodeChangeQuery,
    RecordTraceCommand,
)
from packages.traceability.domain.models import (
    CausalNode,
    CodeLocation,
    TraceabilityChainAggregate,
)
from packages.traceability.domain.ports import TraceabilityRepositoryPort


class RecordCodeChangeTraceUseCase:
    def __init__(self, repository: TraceabilityRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: RecordTraceCommand) -> None:
        location = CodeLocation(
            file_path=command.file_path,
            start_line=command.start_line,
            end_line=command.end_line,
            commit_hash=command.commit_hash,
        )

        chain = TraceabilityChainAggregate(
            trace_id=command.trace_id, target_location=location
        )

        for dto in command.nodes:
            chain.add_causal_node(
                CausalNode(
                    node_id=dto.node_id,
                    node_type=dto.node_type,
                    title=dto.title,
                    description=dto.description,
                    evidence_payload=dto.evidence_payload,
                )
            )

        self._repository.save(chain)


class ExplainCodeChangeUseCase:
    """Answers the question: Why did the AI modify this line of code?"""

    def __init__(self, repository: TraceabilityRepositoryPort) -> None:
        self._repository = repository

    def execute(
        self, query: ExplainCodeChangeQuery
    ) -> CodeChangeExplanationResponse:
        chain = self._repository.find_by_location(
            file_path=query.file_path, line_number=query.line_number
        )

        if chain is None:
            return CodeChangeExplanationResponse(
                trace_id=None,
                file_path=str(query.file_path),
                line_number=query.line_number,
                explanation=(
                    f"No AI decision trace found for "
                    f"{query.file_path}:{query.line_number}."
                ),
                found=False,
            )

        explanation = chain.generate_explanation()

        return CodeChangeExplanationResponse(
            trace_id=chain.trace_id,
            file_path=str(query.file_path),
            line_number=query.line_number,
            explanation=explanation,
            found=True,
        )
