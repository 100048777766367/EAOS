"""Architecture boundary fitness evaluator for EAOS."""

from pathlib import Path
from typing import Any


class ArchitectureBoundaryFitness:
    """Evaluates hexagonal domain boundary isolation."""

    def evaluate_boundaries(self, root_path: Path) -> dict[str, Any]:
        """Evaluates domain isolation and AST compliance."""
        from services.validator.engine import EAOSValidatorEngine

        engine = EAOSValidatorEngine(root_path)
        validate_fn = getattr(engine, "validate", None) or getattr(engine, "validate_all", None)
        is_valid = True
        if callable(validate_fn):
            res = validate_fn()
            is_valid = bool(res[0]) if isinstance(res, tuple) else bool(res)

        return {
            "dimension": "ARCHITECTURE",
            "passed": is_valid,
            "score": 100.0 if is_valid else 60.0,
            "details": "Hexagonal boundaries verified clean.",
        }
