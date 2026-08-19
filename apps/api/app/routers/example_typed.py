"""Sample strict-typed router for EAOS API Gateway."""

from typing import Annotated, Any

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field


class TypedRequestDTO(BaseModel):
    """DTO nhận dữ liệu với Pydantic v2."""

    action_id: str = Field(..., description="Mã hành động")
    payload: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)


class TypedResponseDTO(BaseModel):
    """DTO phản hồi với Type Annotations đầy đủ."""

    status: str
    processed_id: str
    result: dict[str, Any]

    model_config = ConfigDict(frozen=True)


router = APIRouter(prefix="/v1/typed-example", tags=["Typed Engine"])


@router.post(
    "/execute",
    response_model=TypedResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def execute_typed_action(
    request_dto: Annotated[TypedRequestDTO, Body(embed=False)],
) -> TypedResponseDTO:
    """Thực thi hành động với kiểm tra kiểu nghiêm ngặt (MyPy Strict Clean)."""
    if not request_dto.action_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="action_id không được để trống",
        )

    return TypedResponseDTO(
        status="SUCCESS",
        processed_id=request_dto.action_id,
        result={"processed": True},
    )
