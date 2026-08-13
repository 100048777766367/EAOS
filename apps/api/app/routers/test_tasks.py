"""Automated testing router for EAOS."""

from __future__ import annotations

import asyncio
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Final

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/testing",
    tags=["Automated Testing Engine"],
)

ROOT_DIR: Final[Path] = Path(__file__).resolve().parents[4]

_TEST_TASKS: Final[dict[str, dict[str, Any]]] = {}


class TestTaskRequest(BaseModel):
    """Testing task request."""

    model_config = ConfigDict(frozen=True)

    task_name: str = Field(
        ...,
        description="Name of the test task",
    )
    target_suite: str = Field(
        default="all",
        description="Test suite",
    )
    auto_fix: bool = Field(
        default=False,
        description="Attempt automatic fixing.",
    )


class TestTaskResponse(BaseModel):
    """Testing task response."""

    model_config = ConfigDict(frozen=True)

    task_id: str
    status: str
    total_tests: int
    passed: int
    failed: int
    coverage: float
    output_log: str


def _run_tests(
    target_suite: str,
) -> tuple[int, int, int, int, str]:
    """Run the requested test suite."""

    if target_suite == "unit":
        target = ROOT_DIR / "tests" / "unit"
    elif target_suite == "integration":
        target = ROOT_DIR / "tests" / "integration"
    else:
        target = ROOT_DIR / "tests"

    if not target.exists():
        return (
            0,
            0,
            0,
            1,
            f"Test target does not exist: {target}",
        )

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(target),
            "-q",
        ],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )

    output = process.stdout

    if process.stderr:
        output = f"{output}\n{process.stderr}".strip()

    passed = 0
    failed = 0

    passed_match = re.search(
        r"(\d+)\s+passed",
        output,
    )

    if passed_match:
        passed = int(passed_match.group(1))

    failed_match = re.search(
        r"(\d+)\s+failed",
        output,
    )

    if failed_match:
        failed = int(failed_match.group(1))

    error_match = re.search(
        r"(\d+)\s+error",
        output,
    )

    if error_match:
        failed += int(error_match.group(1))

    total = passed + failed

    return (
        total,
        passed,
        failed,
        process.returncode,
        output[-8000:],
    )


@router.post(
    "/run",
    response_model=TestTaskResponse,
)
async def run_test_task(
    payload: TestTaskRequest,
) -> TestTaskResponse:
    """Execute a real pytest task."""

    task_id = f"test-{len(_TEST_TASKS) + 1:04d}"

    try:
        (
            total,
            passed,
            failed,
            returncode,
            output,
        ) = await asyncio.to_thread(
            _run_tests,
            payload.target_suite,
        )
    except subprocess.TimeoutExpired:
        total = 0
        passed = 0
        failed = 0
        returncode = 124
        output = "Pytest timed out after 300 seconds."

    status_value = "PASSED" if returncode == 0 and failed == 0 and total > 0 else "FAILED"

    result = TestTaskResponse(
        task_id=task_id,
        status=status_value,
        total_tests=total,
        passed=passed,
        failed=failed,
        coverage=0.0,
        output_log=output,
    )

    _TEST_TASKS[task_id] = result.model_dump()

    return result


@router.get(
    "/status/{task_id}",
    response_model=TestTaskResponse,
)
async def get_test_task_status(
    task_id: str,
) -> TestTaskResponse:
    """Retrieve one test task."""

    if task_id not in _TEST_TASKS:
        raise HTTPException(
            status_code=404,
            detail=f"Test task '{task_id}' not found",
        )

    return TestTaskResponse(
        **_TEST_TASKS[task_id],
    )


@router.get("/tasks")
async def list_test_tasks(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
) -> list[dict[str, Any]]:
    """List recent test tasks."""

    return list(_TEST_TASKS.values())[:limit]
