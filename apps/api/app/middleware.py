from fastapi import FastAPI

"""Middleware registration for EAOS API Gateway."""


def register_middlewares(app: FastAPI) -> None:
    """Registers global security, tracing, and observability middlewares."""
