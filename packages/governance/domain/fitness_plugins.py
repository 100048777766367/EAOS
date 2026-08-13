from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, ConfigDict

from packages.governance.domain.ports import KnowledgeGraphPort

"""Plugin Registry supporting Multi-Artifact Architecture Rules."""


class FitnessRuleMetadata(BaseModel):
    """Metadata describing an independent architecture fitness rule."""

    model_config = ConfigDict(frozen=True)

    rule_id: str
    name: str
    version: str
    category: str  # "CODE", "KNOWLEDGE_GRAPH", "OPENAPI", "ADR"
    description: str


class FitnessRuleResult(BaseModel):
    """Value object for fitness rule evaluation result."""

    model_config = ConfigDict(frozen=True)

    rule_id: str
    passed: bool
    violations_count: int
    details: list[str]


class AbstractFitnessRulePlugin(ABC):
    """Abstract plugin interface for architecture fitness rules."""

    @property
    @abstractmethod
    def metadata(self) -> FitnessRuleMetadata: ...

    @abstractmethod
    def evaluate(self, import_records: list[tuple[str, str]]) -> FitnessRuleResult: ...


class HexagonalBoundaryFitnessRule(AbstractFitnessRulePlugin):
    """Plugin verifying Hexagonal Architecture boundaries."""

    @property
    def metadata(self) -> FitnessRuleMetadata:
        return FitnessRuleMetadata(
            rule_id="hexagonal_boundary",
            name="Hexagonal Boundary Rule",
            version="1.0.0",
            category="CODE",
            description="Ensures domain layer does not import infrastructure.",
        )

    def evaluate(self, import_records: list[tuple[str, str]]) -> FitnessRuleResult:
        violations: list[str] = []
        for file_path, imported_mod in import_records:
            if "domain" in file_path and ("infrastructure" in imported_mod or "fastapi" in imported_mod):
                violations.append(f"{file_path} -> {imported_mod}")

        return FitnessRuleResult(
            rule_id=self.metadata.rule_id,
            passed=len(violations) == 0,
            violations_count=len(violations),
            details=violations,
        )


class KnowledgeGraphIntegrityFitnessRule(AbstractFitnessRulePlugin):
    """Plugin verifying live Knowledge Graph node count in Neo4j."""

    def __init__(self, kg_port: KnowledgeGraphPort | None = None) -> None:
        self.kg_port = kg_port

    @property
    def metadata(self) -> FitnessRuleMetadata:
        return FitnessRuleMetadata(
            rule_id="knowledge_graph_integrity",
            name="Knowledge Graph Integrity Rule",
            version="1.0.0",
            category="KNOWLEDGE_GRAPH",
            description="Verifies Knowledge Graph contains at least 10 nodes.",
        )

    def evaluate(self, import_records: list[tuple[str, str]]) -> FitnessRuleResult:
        violations: list[str] = []
        if self.kg_port is None:
            return FitnessRuleResult(
                rule_id=self.metadata.rule_id,
                passed=True,
                violations_count=0,
                details=["KnowledgeGraphPort not provided, evaluation skipped."],
            )

        try:
            count = self.kg_port.query_system_node_count()
            if count < 10:
                violations.append(f"Knowledge Graph node count insufficient ({count} < 10)")
            details = [f"Verified Neo4j Knowledge Graph ({count} active nodes)."]
        except Exception as e:
            violations.append(f"Failed to query Neo4j Knowledge Graph: {e}")
            details = violations

        return FitnessRuleResult(
            rule_id=self.metadata.rule_id,
            passed=len(violations) == 0,
            violations_count=len(violations),
            details=details,
        )


class FitnessRuleRegistry:
    """Registry supporting dynamic plugin discovery and execution."""

    def __init__(self) -> None:
        self._plugins: dict[str, AbstractFitnessRulePlugin] = {}

    def register(self, plugin: AbstractFitnessRulePlugin) -> None:
        self._plugins[plugin.metadata.rule_id] = plugin

    def get_all_plugins(self) -> list[AbstractFitnessRulePlugin]:
        return list(self._plugins.values())


class GenericGovernancePolicyEngine:
    """Calculates score dynamically without rule-specific hardcoding."""

    def calculate_score(
        self,
        fitness_results: list[FitnessRuleResult],
        empty_dirs_count: int,
        diagnostics_count: int,
        policy: dict[str, Any],
    ) -> float:
        base_score = float(policy.get("base_health_score", 100.0))
        rules_cfg = policy.get("fitness_rules", {})
        total_penalty = 0.0

        for res in fitness_results:
            rule_cfg = rules_cfg.get(res.rule_id, {})
            if rule_cfg.get("enabled", True):
                penalty = float(rule_cfg.get("penalty_per_violation", 10.0))
                total_penalty += res.violations_count * penalty

        dir_cfg = rules_cfg.get("empty_directory", {})
        total_penalty += empty_dirs_count * float(dir_cfg.get("penalty_per_directory", 2.0))
        total_penalty += diagnostics_count * 1.0

        return max(0.0, base_score - total_penalty)
