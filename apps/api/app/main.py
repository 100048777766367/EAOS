"""EAOS Main API Gateway Assembly.

Exposes core, governance, federation, sandbox, security, metrics, and intelligence APIs.
"""

from importlib import import_module, util
from typing import Any, Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from apps.api.app.exception_handlers import custom_api_exception_handler
from apps.api.app.lifespan import api_app_lifespan
from apps.api.app.routers.dashboard import router as dashboard_router
from apps.api.app.routers.identity import router as identity_router
from apps.api.app.routers.master_routes import master_router
from apps.api.app.routers.tasks import router as tasks_router
from apps.api.app.settings import api_settings
from apps.api.middleware.policy_middleware import PolicyEnforcementMiddleware


def expose_metrics(app: FastAPI) -> None:
    """Expose metrics when the optional instrumentator package is installed."""

    if util.find_spec("prometheus_fastapi_instrumentator") is None:
        return
    module = import_module("prometheus_fastapi_instrumentator")
    instrumentator: Any = module.Instrumentator()
    instrumentator.instrument(app).expose(app, endpoint="/metrics")


def create_api_app() -> FastAPI:
    """Constructs and assembles the EAOS API Gateway."""
    app: Final[FastAPI] = FastAPI(
        title=api_settings.title,
        version=api_settings.version,
        lifespan=api_app_lifespan,
    )

    # Middlewares
    # 1. CORS Middleware (Cho phép Web UI ở cổng 3002/4000 giao tiếp với API Gateway)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Policy Guard Middleware
    app.add_middleware(PolicyEnforcementMiddleware)

    # Exception Handlers
    app.add_exception_handler(StarletteHTTPException, custom_api_exception_handler)

    # Routers Assembly
    app.include_router(dashboard_router)
    app.include_router(tasks_router)
    app.include_router(identity_router)
    app.include_router(master_router)

    # Expose Prometheus /metrics endpoint (Fixes 404 logs & enables observability)
    expose_metrics(app)

    return app


app: Final[FastAPI] = create_api_app()
