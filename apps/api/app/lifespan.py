"""API Application Lifespan Events Manager."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

logger = structlog.get_logger()


@asynccontextmanager
async def api_app_lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Manages API Gateway Application startup and shutdown lifecycles."""
    logger.info("Initializing EAOS API Gateway...", version=app.version)
    yield
    logger.info("Shutting down EAOS API Gateway gracefully...")
