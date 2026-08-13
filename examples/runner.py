from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from examples.hello_eaos.hello_world import run_hello_eaos_example
from examples.knowledge.knowledge_example import run_knowledge_example
from examples.policy.policy_example import run_policy_example
from examples.services.service_example import run_service_example
from examples.workflow.workflow_example import run_workflow_example

"""Master Executable Examples Runner."""


class ExamplesExecutionSummaryDTO(BaseModel):
    """Summary DTO for master examples execution."""

    model_config = ConfigDict(frozen=True)

    total_examples_run: int = Field(default=5)
    all_passed: bool = Field(default=True)


class EAOSExamplesRunner:
    """Runner executing all 5 standard EAOS examples."""

    def run_all_examples(self) -> ExamplesExecutionSummaryDTO:
        """Run all starter examples and verify execution."""
        res1 = run_hello_eaos_example()
        res2 = run_knowledge_example("Banking")
        res3 = run_policy_example("DEPLOY")
        res4 = run_service_example(Decimal(10000000))
        res5 = run_workflow_example("Refactor Auth")

        passed = (
            res1.status == "SUCCESS"
            and res2.nodes_found > 0
            and res3.allowed is True
            and res4.status == "COMPLETED"
            and res5.success is True
        )

        return ExamplesExecutionSummaryDTO(total_examples_run=5, all_passed=passed)


if __name__ == "__main__":
    runner = EAOSExamplesRunner()
    summary = runner.run_all_examples()
    print(f"EAOS Examples Runner Complete: All Passed={summary.all_passed}")
