"""Application use cases for Policy Engine."""

from datetime import UTC, datetime

from packages.policy_engine.application.dto import (
    EvaluatePolicyCommand,
    PolicyEvaluationResultDTO,
    RegisterPolicyCommand,
)
from packages.policy_engine.domain.models import (
    PolicyDocumentAggregate,
    PolicyRule,
    RuleCondition,
)
from packages.policy_engine.domain.ports import PolicyRepositoryPort


class RegisterPolicyUseCase:
    def __init__(self, repository: PolicyRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: RegisterPolicyCommand) -> None:
        policy = PolicyDocumentAggregate(
            policy_id=command.policy_id,
            name=command.name,
            description=command.description,
        )

        for r_dto in command.rules:
            condition = RuleCondition(
                field_path=r_dto.condition.field_path,
                operator=r_dto.condition.operator,
                expected_value=r_dto.condition.expected_value,
            )
            rule = PolicyRule(
                rule_id=r_dto.rule_id,
                name=r_dto.name,
                effect=r_dto.effect,
                condition=condition,
                failure_message=r_dto.failure_message,
            )
            policy.add_rule(rule)

        self._repository.save(policy)


class EvaluatePolicyUseCase:
    """Executes deterministic policy validation against provided payload context."""

    def __init__(self, repository: PolicyRepositoryPort) -> None:
        self._repository = repository

    def execute(self, command: EvaluatePolicyCommand) -> PolicyEvaluationResultDTO:
        policy = self._repository.find_by_id(command.policy_id)
        if policy is None:
            raise ValueError(f"Policy {command.policy_id} không tồn tại.")

        is_allowed, violations = policy.evaluate(command.context_payload)

        return PolicyEvaluationResultDTO(
            policy_id=policy.policy_id,
            is_allowed=is_allowed,
            violations=[
                {
                    "rule_id": v.rule_id,
                    "rule_name": v.rule_name,
                    "message": v.message,
                }
                for v in violations
            ],
            evaluated_at=datetime.now(UTC).isoformat(),
        )
