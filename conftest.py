import asyncio
import contextlib
import sys

import pytest

# conftest.py


@pytest.fixture(autouse=True)
def configure_playwright_event_loop(request: pytest.FixtureRequest):
    """Chỉ kích hoạt Proactor policy khi chạy các bài test UI/Playwright."""
    if sys.platform == "win32" and "playwright" in request.fixturenames:
        with contextlib.suppress(Exception):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
