import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

"""Web UI Security and Performance Middleware."""


class WebSecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Applies security headers and timing metrics to all Web UI responses."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Process HTTP request and attach security headers."""
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response
