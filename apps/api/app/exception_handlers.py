"""API Exception Handlers."""

from fastapi import Request, status
from fastapi.responses import JSONResponse


async def custom_api_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handles API exceptions returning JSON error payloads."""
    status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    detail = getattr(exc, "detail", str(exc))
    return JSONResponse(
        status_code=status_code,
        content={"status": "ERROR", "code": status_code, "detail": detail},
    )
