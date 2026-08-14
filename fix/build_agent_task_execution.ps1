# EAOS Agent Task / Execution Subsystem
# UTF-8 No BOM
# Safe rebuild with deterministic repository-root discovery.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Content
    )

    $parent = Split-Path -Parent $Path
    if ($parent) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }

    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

function Backup-IfExists {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$BackupRoot
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return
    }

    $relative = [System.IO.Path]::GetRelativePath($Root, $Path)
    $destination = Join-Path $BackupRoot $relative
    $destinationParent = Split-Path -Parent $destination
    New-Item -ItemType Directory -Force -Path $destinationParent | Out-Null
    Copy-Item -LiteralPath $Path -Destination $destination -Force
    Write-Host "BACKUP  $relative -> $destination"
}

function Write-FileSafe {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RelativePath,
        [Parameter(Mandatory = $true)]
        [string]$Content,
        [Parameter(Mandatory = $true)]
        [string]$BackupRoot
    )

    $target = Join-Path $Root $RelativePath
    Backup-IfExists -Path $target -BackupRoot $BackupRoot
    Write-Utf8NoBom -Path $target -Content $Content
    Write-Host "CREATED $target"
}

function Assert-Ok {
    param(
        [Parameter(Mandatory = $true)]
        [bool]$Condition,
        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    if (-not $Condition) {
        throw $Message
    }
}

# Resolve repository root from this script location.
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$Python = Join-Path $Root ".venv\Scripts\python.exe"

Assert-Ok (Test-Path -LiteralPath $Python -PathType Leaf) `
    "EAOS virtualenv Python not found: $Python"

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupRoot = Join-Path $Root ".eaos\checkpoints\agent-task-execution-backups\$stamp"

Write-Host ""
Write-Host "=============================================="
Write-Host " EAOS AGENT TASK / EXECUTION SUBSYSTEM"
Write-Host "=============================================="
Write-Host "ROOT:   $Root"
Write-Host "PYTHON: $Python"
Write-Host ""

Write-Host "[1/10] Creating directories..."
$directories = @(
    "AGENTS",
    "AGENTS\task_execution",
    "AGENTS\task_execution\ports",
    "AGENTS\task_execution\execution",
    "AGENTS\task_execution\planning",
    "AGENTS\task_execution\tests"
)
foreach ($dir in $directories) {
    New-Item -ItemType Directory -Force -Path (Join-Path $Root $dir) | Out-Null
}

Write-Host "[2/10] Writing package files..."
$init = @'
"""EAOS autonomous agent subsystem."""

from .orchestrator import AgentOrchestrator

__all__ = ["AgentOrchestrator"]
'@

$taskInit = @'
"""EAOS task execution package."""

from .models import AgentTask, TaskResult, TaskState

__all__ = ["AgentTask", "TaskResult", "TaskState"]
'@

$portsInit = @'
"""Execution ports."""

from .executor import ExecutorPort
from .mutation import MutationPort

__all__ = ["ExecutorPort", "MutationPort"]
'@

$executionInit = @'
"""Execution implementations."""
'@

$planningInit = @'
"""Planning boundary."""
'@

Write-FileSafe "AGENTS\__init__.py" $init $BackupRoot
Write-FileSafe "AGENTS\task_execution\__init__.py" $taskInit $BackupRoot
Write-FileSafe "AGENTS\task_execution\ports\__init__.py" $portsInit $BackupRoot
Write-FileSafe "AGENTS\task_execution\execution\__init__.py" $executionInit $BackupRoot
Write-FileSafe "AGENTS\task_execution\planning\__init__.py" $planningInit $BackupRoot

Write-Host "[3/10] Writing task models..."
$models = @'
"""Domain models for agent tasks."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class TaskState(StrEnum):
    """Lifecycle states for an agent task."""

    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    RUNNING = "RUNNING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass(slots=True, frozen=True)
class AgentTask:
    """Immutable task request."""

    task_id: str
    goal: str
    agent_id: str = "coder"


@dataclass(slots=True, frozen=True)
class TaskResult:
    """Execution result."""

    task_id: str
    state: TaskState
    output: str = ""
    error: str | None = None
    evidence_id: str | None = None


__all__ = ["AgentTask", "TaskResult", "TaskState"]
'@
Write-FileSafe "AGENTS\task_execution\models.py" $models $BackupRoot

Write-Host "[4/10] Writing ports..."
$executorPort = @'
"""Executor port."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path
from typing import Protocol

from ..models import AgentTask


class ExecutorPort(Protocol):
    """Boundary for task execution."""

    async def execute(
        self,
        task: AgentTask,
        project_root: Path,
    ) -> AsyncIterator[dict[str, object]]:
        """Execute a task and emit events."""
        ...
'@

$mutationPort = @'
"""Repository mutation boundary."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class MutationPort(Protocol):
    """Boundary for governed repository mutations."""

    async def apply(
        self,
        project_root: Path,
        patch: str,
    ) -> str:
        """Apply a previously approved mutation."""
        ...
'@

Write-FileSafe "AGENTS\task_execution\ports\executor.py" $executorPort $BackupRoot
Write-FileSafe "AGENTS\task_execution\ports\mutation.py" $mutationPort $BackupRoot

Write-Host "[5/10] Writing planning boundary..."
$planner = @'
"""Task planning boundary."""

from __future__ import annotations

from dataclasses import dataclass

from ..models import AgentTask


@dataclass(slots=True, frozen=True)
class TaskPlan:
    """Minimal executable plan."""

    task: AgentTask
    steps: tuple[str, ...]


class TaskPlanner:
    """Create deterministic task plans."""

    def plan(self, task: AgentTask) -> TaskPlan:
        """Build a minimal plan without mutating the repository."""
        return TaskPlan(
            task=task,
            steps=(
                "inspect",
                "execute",
                "verify",
            ),
        )
'@
Write-FileSafe "AGENTS\task_execution\planning\planner.py" $planner $BackupRoot

Write-Host "[6/10] Writing execution engine..."
$executor = @'
"""Task execution engine."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

from ..models import AgentTask, TaskState
from ..planning.planner import TaskPlanner


class TaskExecutor:
    """Execute the safe task lifecycle boundary."""

    def __init__(self) -> None:
        self.planner = TaskPlanner()

    async def execute(
        self,
        task: AgentTask,
        project_root: Path,
    ) -> AsyncIterator[dict[str, object]]:
        """Execute planning and emit lifecycle events."""
        plan = self.planner.plan(task)

        yield {
            "type": "agent_task",
            "state": TaskState.PLANNING.value,
            "task_id": plan.task.task_id,
            "steps": list(plan.steps),
        }

        yield {
            "type": "agent_task",
            "state": TaskState.RUNNING.value,
            "task_id": task.task_id,
            "message": "Execution boundary ready.",
        }

        yield {
            "type": "agent_task",
            "state": TaskState.VERIFYING.value,
            "task_id": task.task_id,
            "message": "Delegating verification to EAOS verification subsystem.",
        }
'@
Write-FileSafe "AGENTS\task_execution\execution\executor.py" $executor $BackupRoot

Write-Host "[7/10] Writing task manager..."
$manager = @'
"""Agent task manager."""

from __future__ import annotations

from uuid import uuid4

from .models import AgentTask


class TaskManager:
    """Create and track agent task identities."""

    def create(
        self,
        goal: str,
        agent_id: str = "coder",
    ) -> AgentTask:
        """Create a new task."""
        return AgentTask(
            task_id=f"tsk-{uuid4().hex[:8]}",
            goal=goal,
            agent_id=agent_id,
        )
'@
Write-FileSafe "AGENTS\task_execution\task_manager.py" $manager $BackupRoot

Write-Host "[8/10] Writing AgentOrchestrator..."
$orchestrator = @'
"""Top-level agent task orchestration."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

from .task_execution.execution.executor import TaskExecutor
from .task_execution.models import AgentTask, TaskState
from .task_execution.task_manager import TaskManager


class AgentOrchestrator:
    """Coordinate task creation and governed execution."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()
        self.manager = TaskManager()
        self.executor = TaskExecutor()

    def create_task(
        self,
        goal: str,
        agent_id: str = "coder",
    ) -> AgentTask:
        """Create a task without executing it."""
        return self.manager.create(goal, agent_id)

    async def execute(
        self,
        task: AgentTask,
    ) -> AsyncIterator[dict[str, object]]:
        """Execute a task through the execution boundary."""
        yield {
            "type": "agent_task",
            "state": TaskState.QUEUED.value,
            "task_id": task.task_id,
            "agent_id": task.agent_id,
        }

        async for event in self.executor.execute(
            task,
            self.project_root,
        ):
            yield event
'@
Write-FileSafe "AGENTS\orchestrator.py" $orchestrator $BackupRoot

$readme = @'
# EAOS Agent Task / Execution

The subsystem separates task management, planning, execution, and
repository mutation boundaries.

Lifecycle:

QUEUED -> PLANNING -> RUNNING -> VERIFYING

Verification remains owned by the EAOS verification subsystem.

This package does not directly mutate repository files. Any mutation must
cross a governed MutationPort and must be approved by the EAOS governance
layer.
'@
Write-FileSafe "AGENTS\task_execution\README.md" $readme $BackupRoot

Write-Host "[9/10] Writing smoke test..."
$test = @'
"""Smoke tests for Agent Task / Execution."""

from pathlib import Path

import pytest

from AGENTS import AgentOrchestrator
from AGENTS.task_execution.models import TaskState


@pytest.mark.asyncio
async def test_agent_task_lifecycle(tmp_path: Path) -> None:
    orchestrator = AgentOrchestrator(tmp_path)
    task = orchestrator.create_task("inspect repository")

    states: list[str] = []
    async for event in orchestrator.execute(task):
        states.append(str(event["state"]))

    assert states == [
        TaskState.QUEUED.value,
        TaskState.PLANNING.value,
        TaskState.RUNNING.value,
        TaskState.VERIFYING.value,
    ]
'@
Write-FileSafe "AGENTS\task_execution\tests\test_task_execution.py" $test $BackupRoot

Write-Host "[10/10] Running validation..."

Write-Host ""
Write-Host "[CHECK 1] Repository path and Python path..."
$env:PYTHONPATH = $Root
$actualRoot = (& $Python -c "from pathlib import Path; print(Path.cwd().resolve())").Trim()
Assert-Ok ($actualRoot -eq $Root) "Python working directory mismatch: $actualRoot"
Write-Host "ROOT/PYTHONPATH OK"

Write-Host ""
Write-Host "[CHECK 2] Python imports..."
$importCode = @'
import sys
from pathlib import Path

root = Path.cwd().resolve()
assert str(root) == str(Path(r"$Root").resolve())
assert str(root) in sys.path or "" in sys.path

from AGENTS import AgentOrchestrator
from AGENTS.task_execution.models import AgentTask, TaskResult, TaskState
from AGENTS.task_execution.task_manager import TaskManager
from AGENTS.task_execution.execution.executor import TaskExecutor
from AGENTS.task_execution.planning.planner import TaskPlanner

assert AgentOrchestrator is not None
assert AgentTask is not None
assert TaskResult is not None
assert TaskState.QUEUED.value == "QUEUED"
assert TaskManager is not None
assert TaskExecutor is not None
assert TaskPlanner is not None

print("IMPORTS OK")
'@
$importCode = $importCode.Replace('$Root', $Root.Replace('\', '\\'))
$importOutput = & $Python -c $importCode 2>&1
if ($LASTEXITCODE -ne 0) {
    $importOutput | ForEach-Object { Write-Host $_ }
    throw "Python import check failed."
}
$importOutput | ForEach-Object { Write-Host $_ }

Write-Host ""
Write-Host "[CHECK 3] UTF-8 No BOM..."
$pythonFiles = Get-ChildItem `
    -LiteralPath (Join-Path $Root "AGENTS") `
    -Recurse `
    -Filter "*.py"

foreach ($file in $pythonFiles) {
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $hasBom = $bytes.Length -ge 3 `
        -and $bytes[0] -eq 0xEF `
        -and $bytes[1] -eq 0xBB `
        -and $bytes[2] -eq 0xBF
    if ($hasBom) {
        throw "UTF-8 BOM detected: $($file.FullName)"
    }
}
Write-Host "UTF-8 No BOM: OK"

Write-Host ""
Write-Host "[CHECK 4] Ruff..."
& $Python -m ruff check `
    (Join-Path $Root "AGENTS")
if ($LASTEXITCODE -ne 0) {
    throw "Ruff validation failed."
}

Write-Host ""
Write-Host "[CHECK 5] Agent task smoke test..."
& $Python -m pytest `
    (Join-Path $Root "AGENTS\task_execution\tests") `
    -q
if ($LASTEXITCODE -ne 0) {
    throw "Agent task smoke test failed."
}

Write-Host ""
Write-Host "[CHECK 6] Direct lifecycle..."
$lifecycleCode = @'
import asyncio
from pathlib import Path

from AGENTS import AgentOrchestrator


async def main() -> None:
    orchestrator = AgentOrchestrator(Path.cwd())
    task = orchestrator.create_task("verification smoke")
    states = []

    async for event in orchestrator.execute(task):
        states.append(event["state"])

    expected = [
        "QUEUED",
        "PLANNING",
        "RUNNING",
        "VERIFYING",
    ]
    assert states == expected, (states, expected)
    print("LIFECYCLE OK")
    print(" -> ".join(states))


asyncio.run(main())
'@
$lifecycleOutput = & $Python -c $lifecycleCode 2>&1
if ($LASTEXITCODE -ne 0) {
    $lifecycleOutput | ForEach-Object { Write-Host $_ }
    throw "Agent task lifecycle failed."
}
$lifecycleOutput | ForEach-Object { Write-Host $_ }

Write-Host ""
Write-Host "[CHECK 7] Existing EAOS verification subsystem..."
$verificationCode = @'
import asyncio
from pathlib import Path

from apps.api.app.services.chat.verification.coordinator import (
    VerificationCoordinator,
)


async def main() -> None:
    result = []
    coordinator = VerificationCoordinator(Path.cwd())

    async for event in coordinator.run():
        result.append(event["type"])

    required = {
        "verification_started",
        "verification_runner_started",
        "verification_runner_result",
        "verification_result",
    }
    assert required.issubset(set(result)), result
    print("VERIFICATION COORDINATOR OK")
    print(" -> ".join(result))


asyncio.run(main())
'@
$verificationOutput = & $Python -c $verificationCode 2>&1
if ($LASTEXITCODE -ne 0) {
    $verificationOutput | ForEach-Object { Write-Host $_ }
    throw "Existing verification subsystem check failed."
}
$verificationOutput | ForEach-Object { Write-Host $_ }

Write-Host ""
Write-Host "[CHECK 8] Package path..."
$packageCheck = & $Python -c "import AGENTS; print(AGENTS.__file__)" 2>&1
if ($LASTEXITCODE -ne 0) {
    $packageCheck | ForEach-Object { Write-Host $_ }
    throw "AGENTS package path check failed."
}
$packageCheck | ForEach-Object { Write-Host $_ }

Write-Host ""
Write-Host "[CHECK 9] Full unit tests..."
& $Python -m pytest `
    (Join-Path $Root "tests\unit") `
    -q
if ($LASTEXITCODE -ne 0) {
    throw "Unit tests failed."
}

Write-Host ""
Write-Host "[CHECK 10] Final architecture..."
Write-Host ""
Write-Host "Agent architecture:"
Write-Host "AgentOrchestrator"
Write-Host " -> TaskManager"
Write-Host " -> TaskPlanner"
Write-Host " -> TaskExecutor"
Write-Host " -> VerificationCoordinator"
Write-Host " -> RuffRunner / PytestRunner"
Write-Host " -> EvidenceStore"
Write-Host ""
Write-Host "Repository mutation:"
Write-Host "AgentExecutor"
Write-Host " -> MutationPort"
Write-Host " -> Governance / Approval boundary"
Write-Host ""
Write-Host "Backup:"
Write-Host $BackupRoot
Write-Host ""
Write-Host "=============================================="
Write-Host " AGENT TASK / EXECUTION BUILD: GREEN"
Write-Host "=============================================="
Write-Host ""
