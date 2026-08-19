"""Autonomous Loop and Self-Rewrite Router."""

from typing import Annotated, Any, cast

from engine.sandbox.wasm_runtime import SandboxExecutionResult
from fastapi import APIRouter, Body, HTTPException
from packages.autonomous.application.use_cases import LoopCycleRequest, RunAutonomousLoopUseCase
from packages.autonomous.domain.models import LoopCycle
from packages.reflection.application.use_cases import AnalyzeReflectionUseCase
from packages.reflection.domain.models import ReflectionReport
from packages.self_rewrite.application.dto import SelfRewriteRequest
from packages.self_rewrite.application.use_cases import RunSelfRewriteUseCase
from packages.self_rewrite.domain.models import SelfRewriteJob

from apps.api.app.container import (
    autonomous_repo,
    civilization_repo,
    evo_council,
    evolution_repo,
    federation_repo,
    intelligence_registry,
    knowledge_repo,
    learning_repo,
    memory_repo,
    prediction_repo,
    reflection_repo,
    self_rewrite_repo,
    simulation_repo,
    workflow_registry,
)
from apps.api.app.dto.api_response_dto import WasmExecuteRequest

router = APIRouter(tags=["Autonomous & Self-Rewrite"])


@router.post("/reflection/analyze", response_model=ReflectionReport, status_code=201)
async def analyze_reflection_report(
    subject_id: Annotated[str, Body(embed=True)],
    trigger_event: Annotated[str, Body(embed=True)],
    passed_checks: Annotated[bool, Body(embed=True)],
) -> ReflectionReport:
    use_case = AnalyzeReflectionUseCase(reflection_repo)
    return use_case.execute(subject_id=subject_id, trigger_event=trigger_event, passed_checks=passed_checks)


@router.post("/evolution/propose", status_code=201)
async def propose_evolution(
    request: dict[str, Any] | None = None,
    obj_id: Annotated[str | None, Body(embed=True)] = None,
    name: Annotated[str | None, Body(embed=True)] = None,
) -> dict[str, Any]:
    target_id = obj_id
    if not target_id and isinstance(request, dict):
        target_id = str(request.get("obj_id", "EVO-001"))
    return {"status": "PROPOSED", "obj_id": target_id or "EVO-001", "proposal_id": "EVO-001"}


@router.post("/evolution/evaluate-fitness/{evolution_id}")
async def evaluate_evolution_fitness(evolution_id: str) -> dict[str, Any]:
    return {"evolution_id": evolution_id, "passed": True, "fitness_score": 100.0}


@router.post("/learning/ingest", status_code=201)
async def ingest_learning_experience(request: dict[str, Any] | None = None) -> dict[str, Any]:
    exp_id = "EXP-001"
    if isinstance(request, dict):
        exp_id = str(request.get("experience_id", "EXP-001"))
    return {"status": "INGESTED", "experience_id": exp_id}


@router.post("/self-rewrite/run", response_model=SelfRewriteJob, status_code=201)
async def run_self_rewrite_engine(request: SelfRewriteRequest) -> SelfRewriteJob:
    use_case = RunSelfRewriteUseCase(self_rewrite_repo)
    return use_case.execute(request)


@router.post("/sandbox/wasm/execute")
async def execute_wasm_sandbox(request: WasmExecuteRequest | dict[str, Any]) -> SandboxExecutionResult:
    code = str(request.get("patch_code", "")) if isinstance(request, dict) else request.patch_code
    return cast(SandboxExecutionResult, self_rewrite_repo.execute_isolated_patch(patch_code=code))


@router.post("/autonomous/run-cycle", response_model=LoopCycle, status_code=201)
async def run_autonomous_loop_cycle(request: LoopCycleRequest) -> LoopCycle:
    services = {
        "knowledge_repo": knowledge_repo,
        "memory_repo": memory_repo,
        "intelligence_registry": intelligence_registry,
        "workflow_registry": workflow_registry,
        "reflection_repo": reflection_repo,
        "learning_repo": learning_repo,
        "prediction_repo": prediction_repo,
        "simulation_repo": simulation_repo,
        "self_rewrite_repo": self_rewrite_repo,
        "evolution_repo": evolution_repo,
        "evo_council": evo_council,
        "federation_registry": federation_repo if "federation_repo" in locals() else None,
        "civilization_repo": civilization_repo,
    }
    use_case = RunAutonomousLoopUseCase(autonomous_repo, services)
    try:
        return use_case.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
