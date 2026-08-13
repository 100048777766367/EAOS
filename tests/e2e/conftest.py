"""E2E Test Conftest for Playwright setup with Pytest-Playwright integration."""

import asyncio
import sys

import pytest

# Phân tách Event Loop Policy: Bắt buộc dùng ProactorEventLoop cho E2E/Playwright trên Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Cấu hình tham số khởi chạy trình duyệt cho pytest-playwright (Headless mặc định)."""
    return {
        **browser_type_launch_args,
        "headless": True,
    }
