"""AIDE middleware registration."""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def install_aide_middleware(app: FastAPI) -> None:
    """Install browser-facing middleware for the AIDE client app."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:6932", "http://localhost:6932"],
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
