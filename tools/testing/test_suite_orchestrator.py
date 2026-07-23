"""Test suite auditor engine analyzing multi-tier testing pyramid tiers."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class TestSuiteSummaryDTO(BaseModel):
    """Value object representing test tier audit results."""

    model_config = ConfigDict(frozen=True)

    tier: str
    file_count: int
    status: str


class TestSuiteAuditorEngine:
    """Auditor discovering and evaluating multi-tier test suites."""

    __test__ = False

    TIERS: tuple[str, ...] = (
        "contract",
        "e2e",
        "integration",
        "performance",
        "unit",
    )

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()
        self.tests_dir: Path = self.root_dir / "tests"

    def audit_test_tiers(self) -> list[TestSuiteSummaryDTO]:
        """Audits all 5 testing pyramid tiers in tests/."""
        results: list[TestSuiteSummaryDTO] = []
        if not self.tests_dir.exists():
            return results

        for tier in self.TIERS:
            tier_dir = self.tests_dir / tier
            file_count = 0

            if tier_dir.exists() and tier_dir.is_dir():
                files = list(tier_dir.rglob("test_*.py"))
                file_count = len(files)

            results.append(
                TestSuiteSummaryDTO(
                    tier=tier,
                    file_count=file_count,
                    status="ACTIVE" if file_count >= 0 else "EMPTY",
                )
            )

        return results
