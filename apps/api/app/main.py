"""EAOS Main API Gateway Assembly.

Exposes core, governance, federation, sandbox, security, metrics,
intelligence, and business capability APIs.
"""

from pathlib import Path
from typing import Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.exceptions import HTTPException as StarletteHTTPException

from apps.api.app.exception_handlers import (
    custom_api_exception_handler,
)
from apps.api.app.lifespan import api_app_lifespan

# ---------------------------------------------------------------------------
# Core & Platform Routers
# ---------------------------------------------------------------------------
from apps.api.app.routers.agent_orchestration_router import (
    router as agent_orchestration_router,
)
from apps.api.app.routers.agents import router as agents_router
from apps.api.app.routers.chat import router as chat_router
from apps.api.app.routers.crm import router as crm_router
from apps.api.app.routers.dashboard import (
    router as dashboard_router,
)
from apps.api.app.routers.digitaltwin_router import (
    router as digitaltwin_router,
)
from apps.api.app.routers.engineering_loop_router import (
    router as engineering_loop_router,
)
from apps.api.app.routers.files import router as files_router
from apps.api.app.routers.finance import router as finance_router
from apps.api.app.routers.identity import router as identity_router
from apps.api.app.routers.marketing import router as marketing_router
from apps.api.app.routers.master_routes import master_router
from apps.api.app.routers.observability_router import (
    router as observability_router,
)
from apps.api.app.routers.open_webui import (
    router as open_webui_router,
)
from apps.api.app.routers.resilience import (
    router as resilience_router,
)
from apps.api.app.routers.runtime_control_router import (
    router as runtime_control_router,
)
from apps.api.app.routers.sales import router as sales_router
from apps.api.app.routers.splay import router as splay_router

# ---------------------------------------------------------------------------
# Chat WebSocket Router
# IMPORTANT:
# WebSocket /ws/chat lives here, NOT in routers/chat.py
# ---------------------------------------------------------------------------
from apps.api.app.services.chat.websocket_service import (
    router as chat_websocket_router,
)
from apps.api.app.settings import api_settings
from apps.api.middleware.policy_middleware import (
    PolicyEnforcementMiddleware,
)


def create_api_app() -> FastAPI:
    """Construct and assemble the EAOS API Gateway."""

    app: Final[FastAPI] = FastAPI(
        title=api_settings.title,
        version=api_settings.version,
        lifespan=api_app_lifespan,
    )

    # -----------------------------------------------------------------------
    # Static files
    # -----------------------------------------------------------------------

    base_dir: Final[Path] = Path(__file__).resolve().parent
    static_dir: Final[Path] = base_dir / "static"

    if static_dir.exists():
        app.mount(
            "/static",
            StaticFiles(directory=str(static_dir)),
            name="static",
        )

    # -----------------------------------------------------------------------
    # Middleware
    # -----------------------------------------------------------------------

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        PolicyEnforcementMiddleware,
    )

    # -----------------------------------------------------------------------
    # Exception handlers
    # -----------------------------------------------------------------------

    app.add_exception_handler(
        StarletteHTTPException,
        custom_api_exception_handler,
    )

    # =======================================================================
    # ROUTERS ASSEMBLY
    # =======================================================================

    # -----------------------------------------------------------------------
    # Files / Dashboard / Identity
    # -----------------------------------------------------------------------

    app.include_router(files_router)
    app.include_router(dashboard_router)
    app.include_router(identity_router)

    # -----------------------------------------------------------------------
    # AI Studio HTTP
    #
    # /chat
    # /v1/runtime/footer
    # -----------------------------------------------------------------------

    app.include_router(chat_router)

    # -----------------------------------------------------------------------
    # AI Studio WebSocket
    #
    # /ws/chat
    #
    # IMPORTANT:
    # This router is intentionally separate from chat_router.
    # -----------------------------------------------------------------------

    app.include_router(chat_websocket_router)

    # -----------------------------------------------------------------------
    # Runtime / Digital Twin / Agent Orchestration
    # -----------------------------------------------------------------------

    app.include_router(runtime_control_router)
    app.include_router(digitaltwin_router)
    app.include_router(agent_orchestration_router)
    app.include_router(open_webui_router)

    # -----------------------------------------------------------------------
    # Master Router
    #
    # Health, Knowledge, Memory, Governance, Security,
    # Telemetry, Chaos, Federation, Tenancy, Intelligence,
    # Autonomous, Capabilities
    # -----------------------------------------------------------------------

    app.include_router(master_router)

    # -----------------------------------------------------------------------
    # Extended Engineering / Resilience
    # -----------------------------------------------------------------------

    app.include_router(observability_router)
    app.include_router(engineering_loop_router)
    app.include_router(resilience_router)
    app.include_router(splay_router)
    app.include_router(agents_router)

    # -----------------------------------------------------------------------
    # Enterprise Business Capabilities
    # -----------------------------------------------------------------------

    app.include_router(crm_router)
    app.include_router(finance_router)
    app.include_router(sales_router)
    app.include_router(marketing_router)

    # -----------------------------------------------------------------------
    # Prometheus
    # -----------------------------------------------------------------------

    Instrumentator().instrument(app).expose(
        app,
        endpoint="/metrics",
    )

    return app


# ---------------------------------------------------------------------------
# ASGI application
# ---------------------------------------------------------------------------

app: Final[FastAPI] = create_api_app()