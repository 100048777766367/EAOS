"""Live demonstration script proving EAOS Enterprise Generation engine."""

import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent.parent
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

from packages.enterprise_generator.application.use_cases import (  # noqa: E402
    GenerateEnterpriseUseCase,
)
from packages.enterprise_generator.domain.models import (  # noqa: E402
    EnterpriseBlueprintSpec,
)


def run_enterprise_generator_demo() -> None:
    """Demonstrates full generation of an AI-Native Enterprise."""
    generator = GenerateEnterpriseUseCase()

    spec = EnterpriseBlueprintSpec(
        enterprise_name="Global AI Commerce",
        industry_type="AI_NATIVE_SAAS",
        selected_capabilities=(
            "marketing",
            "crm",
            "sales",
            "finance",
            "content",
            "knowledge",
        ),
        deployment_target="CLOUD_CONTAINER",
    )

    output = generator.execute(spec)

    print("====================================================")
    print(" EAOS ENTERPRISE GENERATOR DEMONSTRATION OUTPUT     ")
    print("====================================================")
    print(f"✔ Enterprise Name      : {output.enterprise_name}")
    print(f"✔ Generation ID        : {output.generation_id}")
    print(f"✔ Packages Generated   : {output.generated_packages_count}")
    print(f"✔ 7-File Specs Created : {output.generated_specs_count}")
    print(f"✔ Constitution Status  : {output.is_constitution_compliant}")
    print("====================================================")


if __name__ == "__main__":
    run_enterprise_generator_demo()
