"""Application Services for Simulation Engine."""

import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from packages.simulation.domain.models import (
    BranchEnvironmentType,
    ComparativeResearchReport,
    EmpiricalEvidence,
    MetricDelta,
    Simulation,
)
from packages.simulation.domain.ports import (
    DigitalTwinSandboxPort,
    ResearchReportRepositoryPort,
)


class SimulationRequest(BaseModel):
    """Yêu cầu thực thi Giả lập Simulation."""

    name: str = Field(default="")
    payload: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class RunSimulationUseCase:
    """Use case thực thi mô phỏng giả lập."""

    def __init__(self, repo: Any = None) -> None:
        self.repo = repo

    def execute(self, request: SimulationRequest) -> Simulation:
        return Simulation(
            id=f"SIM-{uuid.uuid4().hex[:6].upper()}",
            status="COMPLETED",
            result={"request_name": request.name},
        )


class RunCounterfactualResearchUseCase:
    """Use Case executing counterfactual experiment on cloned twin branches."""

    def __init__(
        self,
        sandbox_adapter: DigitalTwinSandboxPort,
        report_repo: ResearchReportRepositoryPort,
    ) -> None:
        self._sandbox = sandbox_adapter
        self._report_repo = report_repo

    def execute_experiment(
        self,
        experiment_name: str,
        base_state: dict[str, Any],
        beta_mutation: dict[str, Any],
        workload_payload: dict[str, Any],
    ) -> ComparativeResearchReport:
        snapshot_id = f"SNAP-{uuid.uuid4().hex[:8].upper()}"
        self._sandbox.create_snapshot(snapshot_id, base_state)

        alpha_id = f"BRANCH-ALPHA-{uuid.uuid4().hex[:6].upper()}"
        self._sandbox.fork_branch(snapshot_id, alpha_id, BranchEnvironmentType.BASELINE_ALPHA)

        beta_id = f"BRANCH-BETA-{uuid.uuid4().hex[:6].upper()}"
        self._sandbox.fork_branch(snapshot_id, beta_id, BranchEnvironmentType.EXPERIMENTAL_BETA)

        alpha_evidence = self._sandbox.execute_workload(alpha_id, workload_payload)

        mutated_workload = workload_payload.copy()
        mutated_workload["_mutation"] = beta_mutation
        beta_evidence = self._sandbox.execute_workload(beta_id, mutated_workload)

        deltas = self._calculate_deltas(alpha_evidence, beta_evidence)

        fitness_delta_pct = round(
            ((beta_evidence.fitness_score - alpha_evidence.fitness_score) / max(0.001, alpha_evidence.fitness_score))
            * 100.0,
            2,
        )

        if fitness_delta_pct > 0 and beta_evidence.error_count <= alpha_evidence.error_count:
            recommendation = (
                f"KHUYẾN NGHỊ ÁP DỤNG: Nhánh Beta cải thiện +{fitness_delta_pct}% "
                f"điểm thể lực kiến trúc và không phát sinh lỗi."
            )
        else:
            recommendation = (
                f"KHUYẾN NGHỊ BÁC BỎ: Nhánh Beta suy thoái {fitness_delta_pct}% "
                f"hoặc phát sinh {beta_evidence.error_count} lỗi mới."
            )

        report = ComparativeResearchReport(
            report_id=f"RPT-{uuid.uuid4().hex[:8].upper()}",
            experiment_name=experiment_name,
            alpha_evidence=alpha_evidence,
            beta_evidence=beta_evidence,
            deltas=deltas,
            overall_recommendation=recommendation,
            fitness_delta_pct=fitness_delta_pct,
        )

        return self._report_repo.save_report(report)

    def _calculate_deltas(self, alpha: EmpiricalEvidence, beta: EmpiricalEvidence) -> list[MetricDelta]:
        deltas: list[MetricDelta] = []

        time_diff = beta.execution_time_ms - alpha.execution_time_ms
        time_pct = (time_diff / max(0.001, alpha.execution_time_ms)) * 100.0
        deltas.append(
            MetricDelta(
                metric_name="Execution Time (ms)",
                alpha_value=alpha.execution_time_ms,
                beta_value=beta.execution_time_ms,
                delta_absolute=round(time_diff, 2),
                delta_percentage=round(time_pct, 2),
                is_improvement=time_diff < 0,
            )
        )

        fit_diff = beta.fitness_score - alpha.fitness_score
        fit_pct = (fit_diff / max(0.001, alpha.fitness_score)) * 100.0
        deltas.append(
            MetricDelta(
                metric_name="Architecture Fitness Score",
                alpha_value=alpha.fitness_score,
                beta_value=beta.fitness_score,
                delta_absolute=round(fit_diff, 2),
                delta_percentage=round(fit_pct, 2),
                is_improvement=fit_diff > 0,
            )
        )

        mem_diff = beta.memory_usage_mb - alpha.memory_usage_mb
        mem_pct = (mem_diff / max(0.001, alpha.memory_usage_mb)) * 100.0
        deltas.append(
            MetricDelta(
                metric_name="RAM Usage (MB)",
                alpha_value=alpha.memory_usage_mb,
                beta_value=beta.memory_usage_mb,
                delta_absolute=round(mem_diff, 2),
                delta_percentage=round(mem_pct, 2),
                is_improvement=mem_diff < 0,
            )
        )

        return deltas
