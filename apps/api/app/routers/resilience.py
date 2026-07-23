"""Resilience router handling Chaos daemon, fault injection, and WASM sandbox."""

from typing import Annotated, Any

from engine.sandbox.wasm_runtime import (
    SandboxExecutionResult,
    WASMSandboxRuntime,
)
from fastapi import APIRouter, Body
from pydantic import BaseModel, ConfigDict
from tools.chaos.chaos_daemon import (
    AutomatedChaosDaemon,
    ChaosDaemonStatusDTO,
)
from tools.chaos.chaos_engine import (
    ChaosEngine,
    ChaosExperimentResult,
)

router = APIRouter(prefix="", tags=["Resilience"])
chaos_daemon = AutomatedChaosDaemon()
wasm_runtime = WASMSandboxRuntime()


class WasmExecuteRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    patch_code: str


@router.post(
    "/chaos/daemon/cycle",
    response_model=ChaosDaemonStatusDTO,
    status_code=200,
)
async def execute_chaos_daemon_cycle() -> ChaosDaemonStatusDTO:
    """Triggers background chaos resilience engineering cycle."""
    return chaos_daemon.run_chaos_cycle()


@router.post("/chaos/inject-fault")
async def inject_chaos_fault(
    request: dict[str, Any] | None = None,
    fault_type: Annotated[str | None, Body(embed=True)] = None,
    target_service: Annotated[str | None, Body(embed=True)] = None,
) -> ChaosExperimentResult:
    f_type = fault_type
    t_service = target_service
    if isinstance(request, dict):
        if not f_type:
            f_type = str(request.get("fault_type", "DATABASE_DISCONNECT"))
        if not t_service:
            t_service = str(request.get("target_service", "CoreService"))

    engine = ChaosEngine()
    return engine.inject_fault(
        fault_type=f_type or "DATABASE_DISCONNECT",
        target_service=t_service or "CoreService",
    )


@router.post("/sandbox/wasm/execute")
async def execute_wasm_sandbox(
    request: WasmExecuteRequest | dict[str, Any],
) -> SandboxExecutionResult:
    code = str(request.get("patch_code", "")) if isinstance(request, dict) else request.patch_code

    return wasm_runtime.execute_isolated_patch(patch_code=code)


@router.get("/performance/concurrency/metrics")
async def get_concurrency_metrics() -> dict[str, Any]:
    from platform_services.performance.async_concurrency import (
        ConcurrencyTuningEngine,
    )

    engine = ConcurrencyTuningEngine()
    return engine.get_metrics_snapshot().model_dump()


@router.post("/performance/splay/batch-evict")
async def batch_evict_splay_cache(
    target_items: Annotated[int, Body(embed=True)] = 1000,
) -> dict[str, Any]:
    from platform_services.performance.async_concurrency import (
        ConcurrencyTuningEngine,
    )

    engine = ConcurrencyTuningEngine()
    return engine.batch_evict_splay_cache(target_items)
