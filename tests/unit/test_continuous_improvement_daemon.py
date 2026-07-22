"""Unit tests for the Continuous Improvement Daemon."""

from pathlib import Path

from kernel.runtime.continuous_improvement import ContinuousImprovementEngine
from packages.feedback.application.use_cases import ProcessFeedbackUseCase
from packages.feedback.infrastructure.adapters import (
    InMemoryFeedbackRepository,
    MockAdaptationHandler,
)
from packages.policy_engine.application.dto import (
    ConditionDTO,
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


def test_continuous_improvement_daemon_single_cycle(tmp_path: Path) -> None:
    # Setup workspace
    packages_dir = tmp_path / "packages"
    (packages_dir / "knowledge").mkdir(parents=True)

    # Setup Policy Engine
    policy_repo = InMemoryPolicyRepository()
    RegisterPolicyUseCase(policy_repo).execute(
        RegisterPolicyCommand(
            policy_id="POL-PROD-GUARD",
            name="Prod Guard Policy",
            description="Production environment guard",
            rules=[
                PolicyRuleDTO(
                    rule_id="R1",
                    name="Environment Check",
                    effect=PolicyEffect.ALLOW,
                    condition=ConditionDTO(
                        field_path="metadata.environment",
                        operator=Operator.EQUALS,
                        expected_value="production",
                    ),
                    failure_message="Environment must be production",
                )
            ],
        )
    )
    evaluate_policy_uc = EvaluatePolicyUseCase(policy_repo)

    # Setup Feedback Engine
    feedback_repo = InMemoryFeedbackRepository()
    adaptation_handler = MockAdaptationHandler()
    process_feedback_uc = ProcessFeedbackUseCase(
        repository=feedback_repo, adaptation_handler=adaptation_handler
    )

    # Instantiate Engine
    engine = ContinuousImprovementEngine(
        root_dir=tmp_path,
        policy_use_case=evaluate_policy_uc,
        feedback_use_case=process_feedback_uc,
    )

    record = engine.run_single_improvement_cycle()

    assert record.cycle_id.startswith("IMP-")
    assert record.architecture_score == 100
    assert record.policy_passed is True
    assert record.adaptation_action is None
    assert len(engine.history) == 1
