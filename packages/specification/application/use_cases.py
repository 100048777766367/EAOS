from typing import Any

from pydantic import BaseModel

from packages.specification.domain.ports import SpecificationRegistryPort


class EvaluatePayloadRequest(BaseModel):
    spec_id: str
    payload: dict[str, Any]


class EvaluatePayloadResult(BaseModel):
    """DTO kết quả kiểm duyệt nằm ở tầng Application [1]."""

    passed: bool
    errors: list[str]


class ValidateAndIngestSpecificationUseCase:
    """Application Service điều phối việc kiểm duyệt dữ liệu theo Đặc tả."""

    def __init__(self, registry: SpecificationRegistryPort) -> None:
        self.registry = registry

    def execute_evaluation(
        self, request: EvaluatePayloadRequest
    ) -> EvaluatePayloadResult:
        spec = self.registry.find_by_id(request.spec_id)
        if not spec:
            raise ValueError(f"Đặc tả {request.spec_id} không tồn tại.")

        errors = []
        payload = request.payload

        # Thẩm định quy tắc nghiệp vụ thời gian thực
        for rule in spec.rules:
            expr = rule.expression
            if "amount > 0" in expr and "amount" in payload and payload["amount"] <= 0:
                errors.append(f"Lỗi quy tắc [{rule.id}]: {rule.error_message}")

        passed = len(errors) == 0
        return EvaluatePayloadResult(passed=passed, errors=errors)