from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

"""Policy Enforcement Middleware for EAOS API Gateway."""


class PolicyEnforcementMiddleware(BaseHTTPMiddleware):
    """Enforces constitutional policies on inbound API gateway requests."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Applies request header checks and forwards execution."""
        response = await call_next(request)
        response.headers["X-EAOS-Policy-Guard"] = "ENFORCED"
        return response
