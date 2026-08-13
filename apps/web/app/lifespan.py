from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

"""Web Application Lifespan Events Manager."""


logger = structlog.get_logger()


@asynccontextmanager
async def web_app_lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Manages Web UI Application startup and shutdown lifecycles."""
    logger.info(
        "Initializing EAOS Web UI Gateway...",
        version=app.version,
    )
    yield
    logger.info("Shutting down EAOS Web UI Gateway gracefully...")
