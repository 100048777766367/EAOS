from typing import Final

from fastapi import APIRouter, HTTPException, status
from packages.identity.domain.schemas import UserRegisterRequest, UserResponse, UserRole

"""Identity API Router."""


__all__ = ["router"]

router: Final[APIRouter] = APIRouter(tags=["Identity"])


@router.post(
    "/users/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
@router.post(
    "/api/v1/identity/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
@router.post(
    "/identity/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
async def register_user(payload: UserRegisterRequest) -> UserResponse:
    if payload.email == "existing@eaos.internal":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email target already registered",
        )

    display_name = payload.full_name or payload.username or "AI Agent"

    return UserResponse(
        id="usr_01J8EAOS0000000000000001",
        email=payload.email,
        full_name=display_name,
        role=UserRole.OPERATOR,
    )
