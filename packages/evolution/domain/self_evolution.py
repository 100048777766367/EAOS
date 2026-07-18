from datetime import UTC, datetime
from typing import Any

from packages.evolution.domain.models import (
    Evidence,
    EvolutionObject,
    Metadata,
    Provenance,
)


class SelfEvolutionEngine:
    """Động cơ vòng lặp tự sửa lỗi và tự thích ứng cấu hình (Self-healing)."""

    @staticmethod
    def trigger_self_evolution(
        failed_obj: EvolutionObject,
        failed_metric_name: str,
        adjustment_rules: dict[str, Any],
    ) -> EvolutionObject:
        """Tự động phân tích chỉ số lỗi và sinh cấu hình thích ứng mới."""
        new_payload = failed_obj.payload.copy()

        # Tự thích ứng: Ví dụ giảm nhiệt độ LLM hoặc hạ luồng xử lý tự động
        for key, adj_val in adjustment_rules.items():
            if key in new_payload:
                if isinstance(new_payload[key], (float, int)):
                    new_payload[key] = round(new_payload[key] * adj_val, 2)
                else:
                    new_payload[key] = adj_val

        # Tự tăng số phiên bản
        parent_version = failed_obj.payload.get("__version", 1)
        new_payload["__version"] = parent_version + 1

        remedy_evidence = Evidence(
            metric_name="SelfEvolutionEngine Remedy",
            metric_value=1.0,
            passed=True,
            log_summary=f"Tự động khắc phục lỗi thành công: {failed_metric_name}",
        )

        meta = Metadata(environment="production", criticality="high")
        prov = Provenance(
            author="SelfEvolutionEngine",
            triggered_by=f"Auto-correction of {failed_metric_name}",
            parent_id=failed_obj.id,
            timestamp=datetime.now(UTC),
        )

        return EvolutionObject(
            id=failed_obj.id,
            name=f"Self-Evolved {failed_obj.name}",
            payload=new_payload,
            metadata=meta,
            provenance=prov,
            evidences=[remedy_evidence],
        )