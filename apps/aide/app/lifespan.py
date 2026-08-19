"""AIDE lifespan hooks."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def aide_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Mark AIDE startup without claiming backend health."""

    app.state.aide_started = True
    yield
