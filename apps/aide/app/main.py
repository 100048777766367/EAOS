"""EAOS AIDE application entrypoint."""

from typing import Final

from apps.aide.app.lifespan import aide_lifespan
from apps.aide.app.middleware import install_aide_middleware
from apps.aide.app.routes.workspace import router as workspace_router
from apps.aide.app.settings import get_settings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def create_aide_app() -> FastAPI:
    """Create the independent AIDE engineering IDE application."""

    settings = get_settings()
    app: Final[FastAPI] = FastAPI(
        title=settings.title,
        version=settings.version,
        lifespan=aide_lifespan,
    )
    install_aide_middleware(app)
    app.mount("/static", StaticFiles(directory="apps/aide/static"), name="static")
    app.include_router(workspace_router)
    return app


app: Final[FastAPI] = create_aide_app()
