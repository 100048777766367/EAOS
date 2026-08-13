"""EAOS Web UI Application Gateway (Upgraded Modular Architecture)."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from apps.web.app.exception_handlers import (
    custom_http_exception_handler,
)
from apps.web.app.lifespan import web_app_lifespan
from apps.web.app.middleware import WebSecurityHeadersMiddleware
from apps.web.app.routers.control_room_router import (
    router as control_room_router,
)
from apps.web.app.routers.health_router import (
    router as health_router,
)
from apps.web.app.routers.telemetry_ui_router import (
    router as telemetry_ui_router,
)
from apps.web.app.settings import web_settings


def create_web_app() -> FastAPI:
    """Constructs and configures the EAOS Web UI Application Gateway."""
    app = FastAPI(
        title=web_settings.title,
        version=web_settings.version,
        debug=web_settings.debug,
        lifespan=web_app_lifespan,
    )

    # Middlewares
    app.add_middleware(WebSecurityHeadersMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    app.add_exception_handler(
        StarletteHTTPException,
        custom_http_exception_handler,
    )

    # Routers
    app.include_router(health_router)
    app.include_router(control_room_router)
    app.include_router(telemetry_ui_router)

    return app


app = create_web_app()
