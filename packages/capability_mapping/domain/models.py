"""Domain models for Business Capability Mapping context."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, auto


class CapabilityMaturityLevel(Enum):
    INITIAL = auto()
    MANAGED = auto()
    DEFINED = auto()
    QUANTITATIVELY_MANAGED = auto()
    OPTIMIZING = auto()


class RealizationType(Enum):
    PACKAGE = auto()
    SERVICE = auto()
    DATABASE = auto()
    EVENT_TOPIC = auto()
    AI_AGENT = auto()


@dataclass(frozen=True, slots=True)
class RealizationBinding:
    target_ref: str  # Ví dụ: "packages/knowledge" hoặc "agent.planner"
    realization_type: RealizationType
    description: str
    is_active: bool = True


@dataclass(frozen=True, slots=True)
class CapabilityHealth:
    coverage_percentage: float
    broken_bindings_count: int
    maturity_level: CapabilityMaturityLevel


@dataclass(slots=True)
class CapabilityMappingAggregate:
    capability_id: str
    capability_name: str
    domain_group: str
    bindings: list[RealizationBinding] = field(default_factory=list)
    maturity_level: CapabilityMaturityLevel = CapabilityMaturityLevel.DEFINED
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    def bind_realization(self, binding: RealizationBinding) -> None:
        """Adds or updates a technical realization binding."""
        self.bindings = [
            b for b in self.bindings if b.target_ref != binding.target_ref
        ]
        self.bindings.append(binding)
        self.updated_at = datetime.now(UTC)

    def calculate_health(
        self, verified_targets: set[str]
    ) -> CapabilityHealth:
        """Evaluates health based on verified physical existing components."""
        if not self.bindings:
            return CapabilityHealth(
                coverage_percentage=0.0,
                broken_bindings_count=0,
                maturity_level=CapabilityMaturityLevel.INITIAL,
            )

        valid_count = sum(
            1 for b in self.bindings if b.target_ref in verified_targets
        )
        broken_count = len(self.bindings) - valid_count
        coverage = (valid_count / len(self.bindings)) * 100.0

        return CapabilityHealth(
            coverage_percentage=round(coverage, 2),
            broken_bindings_count=broken_count,
            maturity_level=self.maturity_level,
        )
