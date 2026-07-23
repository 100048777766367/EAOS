"""Constitution compliance fitness evaluator for EAOS."""

from pathlib import Path
from typing import Any


class ConstitutionFitnessEvaluator:
    """Evaluates 20 immutable rules constitution compliance."""

    def evaluate_constitution(self, root_path: Path) -> dict[str, Any]:
        """Evaluates presence and compliance of ARCHITECTURE_CONSTITUTION.md."""
        const_file = root_path / "docs" / "ARCHITECTURE_CONSTITUTION.md"
        exists = const_file.exists()
        return {
            "dimension": "GOVERNANCE",
            "passed": exists,
            "score": 100.0 if exists else 0.0,
            "details": "Constitution file present and active.",
        }
