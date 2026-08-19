"""FastAPI dependencies for AIDE."""

from collections.abc import Iterator

from apps.aide.app.settings import AideSettings, get_settings


def aide_settings() -> Iterator[AideSettings]:
    """Yield AIDE settings through FastAPI dependency injection."""

    yield get_settings()
