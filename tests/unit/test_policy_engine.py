"""Unit tests for Policy Engine context."""


from packages.policy_engine.application.dto import (
    ConditionDTO,
    EvaluatePolicyCommand,
    PolicyRuleDTO,
    RegisterPolicyCommand,
)
from packages.policy_engine.application.use_cases import (
    EvaluatePolicyUseCase,
    RegisterPolicyUseCase,
)
from packages.policy_engine.domain.models import Operator, PolicyEffect
from packages.policy_engine.infrastructure.adapters import (
    InMemoryPolicyRepository,
)


def test_policy_evaluation_allow_and_deny_rules() -> None:
    repo = InMemoryPolicyRepository()
    register_uc = RegisterPolicyUseCase(repo)
    evaluate_uc = EvaluatePolicyUseCase(repo)

    # 1. Register Policy requiring production environment and max_retries <= 5
    cmd = RegisterPolicyCommand(
        policy_id="POL-PROD-GUARD",
        name="Production Safety Policy",
        description="Enforces production environment rules",
        rules=[
            PolicyRuleDTO(
                rule_id="RULE-ENV",
                name="Environment Check",
                effect=PolicyEffect.ALLOW,
                condition=ConditionDTO(
                    field_path="metadata.environment",
                    operator=Operator.EQUALS,
                    expected_value="production",
                ),
                failure_message="Môi trường vận hành bắt buộc phải là production.",
            ),
            PolicyRuleDTO(
                rule_id="RULE-RETRY",
                name="Max Retry Limit",
                effect=PolicyEffect.ALLOW,
                condition=ConditionDTO(
                    field_path="payload.max_retry_loops",
                    operator=Operator.LESS_THAN,
                    expected_value=10,
                ),
                failure_message="Số lần thử lại quá lớn (>10) bị cấm.",
            ),
        ],
    )
    register_uc.execute(cmd)

    # 2. Evaluate valid context -> ALLOWED
    valid_ctx = {
        "metadata": {"environment": "production"},
        "payload": {"max_retry_loops": 5},
    }
    res_valid = evaluate_uc.execute(
        EvaluatePolicyCommand(
            policy_id="POL-PROD-GUARD", context_payload=valid_ctx
        )
    )

    assert res_valid.is_allowed is True
    assert len(res_valid.violations) == 0

    # 3. Evaluate invalid context (staging env & max_retries = 15) -> DENIED
    invalid_ctx = {
        "metadata": {"environment": "staging"},
        "payload": {"max_retry_loops": 15},
    }
    res_invalid = evaluate_uc.execute(
        EvaluatePolicyCommand(
            policy_id="POL-PROD-GUARD", context_payload=invalid_ctx
        )
    )

    assert res_invalid.is_allowed is False
    assert len(res_invalid.violations) == 2
    assert res_invalid.violations[0]["rule_id"] == "RULE-ENV"
    assert res_invalid.violations[1]["rule_id"] == "RULE-RETRY"
