from pathlib import Path
from typing import Any

from tools.metrics.architecture_metrics_calculator import (
    ArchitectureMetricsCalculator,
)
from tools.validate.architecture_validator import ArchitectureValidator


class DigitalTwinOrchestrator:
    """Bộ điều phối Bản Sao Số (Digital Twin) để giả lập trước khi Rollout."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir

    def evaluate_proposal(self, proposal: dict[str, Any]) -> dict[str, Any]:
        """Chạy giả lập proposal trên bản sao số để đưa ra quyết định."""
        # 1. Tính toán điểm số hiện tại của hệ thống thật (Reality)
        metrics_calc = ArchitectureMetricsCalculator(self.root_dir)
        metrics_calc.calculate_all()
        current_score = metrics_calc.architecture_score

        # 2. Giả lập tích hợp đề xuất (Proposal) vào Bản sao số (Digital Twin)
        proposed_pkg = proposal.get("package_name", "proposed-module")
        proposed_deps = proposal.get("dependencies", [])
        proposed_layer = proposal.get("layer", "infrastructure")

        # 3. Chạy giả lập chẩn đoán ranh giới kiến trúc ảo
        validator = ArchitectureValidator(self.root_dir)
        validator.run_all_checks()
        simulated_violations = list(validator.violations)

        # Mô phỏng kiểm tra vi phạm ranh giới của đề xuất mới
        LAYER_PRIORITY = {
            "domain": 0,
            "application": 1,
            "infrastructure": 2,
        }
        proposed_pri = LAYER_PRIORITY.get(proposed_layer.lower(), 99)

        # Sửa lỗi PERF401 bằng cách chuyển đổi vòng lặp append thành extend
        extra_violations = [
            (
                f"Layer Violation (Simulated): '{proposed_pkg}' "
                "(domain) illegally depends on infrastructure."
            )
            for dep in proposed_deps
            if proposed_pri == 0 and dep == "infrastructure"
        ]
        simulated_violations.extend(extra_violations)

        # 4. Tính toán điểm số kiến trúc giả lập (Simulated Score)
        simulated_score = current_score
        if len(simulated_violations) > len(validator.violations):
            simulated_score = max(0, simulated_score - 15)

        score_delta = simulated_score - current_score

        # 5. Đưa ra Quyết định tự trị (Decision)
        status = "APPROVED"
        recommendations = []

        if simulated_score < 80:
            status = "REJECTED"
            recommendations.append(
                "Từ chối Rollout: Điểm số sức khỏe giả lập sụt giảm dưới 80."
            )
        if len(simulated_violations) > len(validator.violations):
            status = "REJECTED"
            recommendations.append(
                "Từ chối Rollout: Phát hiện vi phạm ranh giới phân lớp giả lập."
            )

        if status == "APPROVED":
            recommendations.append(
                "Phê duyệt Rollout: Thay đổi an toàn, điểm số đạt chuẩn."
            )

        return {
            "status": status,
            "current_score": current_score,
            "simulated_score": simulated_score,
            "score_delta": score_delta,
            "simulated_violations": simulated_violations,
            "recommendations": recommendations,
            "proposal_details": {
                "package_name": proposed_pkg,
                "layer": proposed_layer,
                "dependencies": proposed_deps,
            },
        }
