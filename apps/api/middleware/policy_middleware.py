"""Policy Enforcement Middleware for API Gateway."""

from typing import Any, ClassVar

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp


class PolicyEnforcementMiddleware(BaseHTTPMiddleware):
    """Middleware enforcing enterprise policies on incoming API requests."""

    EXEMPT_PATHS: ClassVar[set[str]] = {
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/dashboard",
    }

    def __init__(
        self,
        app: ASGIApp,
        evaluate_policy_use_case: Any = None,
        policy_id: str = "",
    ) -> None:
        super().__init__(app)
        self.evaluate_policy_use_case = evaluate_policy_use_case
        self.policy_id = policy_id

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)

        env_header = request.headers.get("X-Environment")
        if env_header and env_header.lower() != "production":
            return JSONResponse(
                status_code=403,
                content={"detail": "Request rejected by EAOS Policy Engine"},
            )

        response = await call_next(request)
        response.headers["X-EAOS-Governance"] = "ENFORCED"
        return response
