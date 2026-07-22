"""Domain models for Enterprise Metrics Engine context."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, auto


class MetricType(Enum):
    MTTR_MINUTES = auto()
    RULE_VIOLATION_COUNT = auto()
    ARCHITECTURE_DRIFT_INDEX = auto()
    POLICY_VIOLATION_COUNT = auto()
    INCIDENT_TREND_RATE = auto()
    AI_SUCCESS_RATE = auto()
    CAPABILITY_HEALTH_SCORE = auto()


@dataclass(frozen=True, slots=True)
class RawMetricObservation:
    observation_id: str
    metric_type: MetricType
    value: float
    target_component: str  # e.g., "packages/knowledge" or "agent.coder"
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class CapabilityHealthScore:
    capability_id: str
    health_score: float  # 0.0 -> 100.0
    active_violations: int
    active_incidents: int
    drift_index: float  # 0.0 (No drift) -> 1.0 (Critical drift)
    status: str  # "HEALTHY" | "DEGRADED" | "CRITICAL"


@dataclass(slots=True)
class ArchitectureHealthAggregate:
    system_id: str
    observations: list[RawMetricObservation] = field(default_factory=list)
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def add_observation(self, obs: RawMetricObservation) -> None:
        self.observations.append(obs)
        self.updated_at = datetime.now(UTC)

    def calculate_mttr(self) -> float:
        """Calculates Mean Time To Recovery in minutes."""
        mttr_obs = [o.value for o in self.observations if o.metric_type == MetricType.MTTR_MINUTES]
        if not mttr_obs:
            return 0.0
        return round(sum(mttr_obs) / len(mttr_obs), 2)

    def calculate_ai_success_rate(self) -> float:
        """Calculates AI Agent self-rewrite/healing success percentage."""
        ai_obs = [o.value for o in self.observations if o.metric_type == MetricType.AI_SUCCESS_RATE]
        if not ai_obs:
            return 100.0  # Default 100% when no failures
        return round((sum(ai_obs) / len(ai_obs)) * 100.0, 2)

    def calculate_architecture_drift_index(self) -> float:
        """Calculates average architectural drift index (0.0 to 1.0)."""
        drift_obs = [o.value for o in self.observations if o.metric_type == MetricType.ARCHITECTURE_DRIFT_INDEX]
        if not drift_obs:
            return 0.0
        return round(sum(drift_obs) / len(drift_obs), 4)

    def evaluate_capability_health(self, capability_id: str) -> CapabilityHealthScore:
        """Calculates health score for a specific business capability."""
        cap_obs = [o for o in self.observations if o.target_component == capability_id]

        violations = sum(int(o.value) for o in cap_obs if o.metric_type == MetricType.RULE_VIOLATION_COUNT)
        incidents = sum(int(o.value) for o in cap_obs if o.metric_type == MetricType.INCIDENT_TREND_RATE)
        drift_vals = [o.value for o in cap_obs if o.metric_type == MetricType.ARCHITECTURE_DRIFT_INDEX]
        avg_drift = sum(drift_vals) / len(drift_vals) if drift_vals else 0.0

        # Base score 100, deduction penalty model
        penalty = (violations * 10.0) + (incidents * 15.0) + (avg_drift * 30.0)
        final_score = max(0.0, min(100.0, 100.0 - penalty))

        if final_score >= 80.0:
            status = "HEALTHY"
        elif final_score >= 50.0:
            status = "DEGRADED"
        else:
            status = "CRITICAL"

        return CapabilityHealthScore(
            capability_id=capability_id,
            health_score=round(final_score, 2),
            active_violations=violations,
            active_incidents=incidents,
            drift_index=round(avg_drift, 4),
            status=status,
        )

    def compute_overall_system_health(self) -> float:
        """Computes system-wide architectural health score (0.0 -> 100.0)."""
        rule_violations = sum(o.value for o in self.observations if o.metric_type == MetricType.RULE_VIOLATION_COUNT)
        policy_violations = sum(
            o.value for o in self.observations if o.metric_type == MetricType.POLICY_VIOLATION_COUNT
        )
        drift_index = self.calculate_architecture_drift_index()
        ai_success = self.calculate_ai_success_rate()

        penalty = (
            (rule_violations * 5.0) + (policy_violations * 5.0) + (drift_index * 40.0) + ((100.0 - ai_success) * 0.3)
        )

        return round(max(0.0, min(100.0, 100.0 - penalty)), 2)
