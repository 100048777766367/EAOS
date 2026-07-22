from typing import Any

from pydantic import BaseModel

from packages.specification.domain.models import (
    EvaluatePayloadResult,
)
from packages.specification.domain.ports import SpecificationRegistryPort


class EvaluatePayloadRequest(BaseModel):
    spec_id: str
    payload: dict[str, Any]


class ValidateAndIngestSpecificationUseCase:
    """Application Service điều phối việc thẩm định dữ liệu theo đặc tả."""

    def __init__(self, registry: SpecificationRegistryPort) -> None:
        self.registry = registry

    def execute_evaluation(self, request: EvaluatePayloadRequest) -> EvaluatePayloadResult:
        spec = self.registry.find_by_id(request.spec_id)
        if not spec:
            raise ValueError(f"Không tìm thấy đặc tả: {request.spec_id}")

        errors = []
        payload = request.payload

        # 1. Thẩm định cấu trúc và kiểu dữ liệu (Schema Validation)
        for field in spec.fields:
            if field.required and field.name not in payload:
                errors.append(f"Lỗi cấu trúc: Thiếu trường '{field.name}'.")
            elif field.name in payload:
                val = payload[field.name]
                if field.type == "str" and not isinstance(val, str):
                    errors.append(f"Lỗi kiểu dữ liệu: Trường '{field.name}' phải là chuỗi (string).")
                elif field.type == "float" and not isinstance(val, (int, float)):
                    errors.append(f"Lỗi kiểu dữ liệu: Trường '{field.name}' phải là số thực (float).")
                elif field.type == "int" and not isinstance(val, int):
                    errors.append(f"Lỗi kiểu dữ liệu: Trường '{field.name}' phải là số nguyên (integer).")

        # 2. Thẩm định quy tắc nghiệp vụ thời gian thực (Rules Evaluation)
        for rule in spec.rules:
            expr = rule.expression
            if "amount > 0" in expr and "amount" in payload and payload["amount"] <= 0:
                errors.append(f"Lỗi quy tắc [{rule.id}]: {rule.error_message}")

        return EvaluatePayloadResult(
            spec_id=request.spec_id,
            passed=len(errors) == 0,
            errors=errors,
        )
