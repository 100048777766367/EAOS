"""API Gateway Router for EAOS Digital Twin System Graph & Impact Analysis."""

from __future__ import annotations

import dataclasses
import time
from typing import Any

from digitaltwin.engine.graph_consistency_auditor import (
    ConsistencyReportDTO,
    ConsistencyViolationDTO,
)
from digitaltwin.engine.graph_delta_checkpoint import GraphDeltaReportDTO
from digitaltwin.engine.impact_analysis_engine import ImpactAnalysisReportDTO
from digitaltwin.models.canonical_graph_model import (
    GraphDomainType,
    GraphNodeType,
    ProvenanceState,
)
from digitaltwin.twin_orchestrator import EnterpriseDigitalTwinOrchestrator
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/v1/digitaltwin", tags=["Digital Twin & System Graph"])

orchestrator = EnterpriseDigitalTwinOrchestrator()


# ─── Request Models ───────────────────────────────────────────────────────────


class ImpactAnalysisRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    target_file: str


class DeltaComparisonRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    before_snapshot_name: str = "BEFORE_MUTATION"
    max_allowed_node_delta: int = 10


class SnapshotSaveRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    snapshot_name: str


class GraphSearchRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    node_type: str | None = None
    domain: str | None = None
    provenance: str | None = None
    name_contains: str | None = None


class SimulationRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    scenario_name: str


# ─── Serialization Helpers ────────────────────────────────────────────────────


def _node_to_dict(node: Any) -> dict[str, Any]:
    """Safely serializes a GraphNodeDTO dataclass to dict."""
    if dataclasses.is_dataclass(node) and not isinstance(node, type):
        return dataclasses.asdict(node)
    return dict(node.__dict__)


def _edge_to_dict(edge: Any) -> dict[str, Any]:
    """Safely serializes a GraphEdgeDTO dataclass to dict."""
    if dataclasses.is_dataclass(edge) and not isinstance(edge, type):
        return dataclasses.asdict(edge)
    return dict(edge.__dict__)


def _violation_to_dict(v: ConsistencyViolationDTO) -> dict[str, Any]:
    if dataclasses.is_dataclass(v) and not isinstance(v, type):
        return dataclasses.asdict(v)
    return dict(v.__dict__)


def _impact_to_dict(r: ImpactAnalysisReportDTO) -> dict[str, Any]:
    if dataclasses.is_dataclass(r) and not isinstance(r, type):
        return dataclasses.asdict(r)
    return dict(r.__dict__)


def _delta_to_dict(r: GraphDeltaReportDTO) -> dict[str, Any]:
    if dataclasses.is_dataclass(r) and not isinstance(r, type):
        return dataclasses.asdict(r)
    return dict(r.__dict__)


def _consistency_to_dict(r: ConsistencyReportDTO) -> dict[str, Any]:
    return {
        "is_consistent": r.is_consistent,
        "total_violations_count": r.total_violations_count,
        "critical_count": r.critical_count,
        "violations": [_violation_to_dict(v) for v in r.violations],
        "timestamp": r.timestamp,
    }


# ─── Endpoints ────────────────────────────────────────────────────────────────


@router.get("/graph")
async def get_system_graph_topology() -> dict[str, Any]:
    """Returns canonical System Graph topology (nodes, edges, provenance summary)."""
    topology = orchestrator.get_system_graph()
    return {
        "twin_id": topology.twin_id,
        "total_nodes": topology.total_nodes,
        "total_edges": topology.total_edges,
        "provenance_summary": topology.provenance_summary,
        "nodes": [_node_to_dict(n) for n in topology.nodes],
        "edges": [_edge_to_dict(e) for e in topology.edges],
        "timestamp": topology.timestamp,
    }


@router.post("/graph/search")
async def search_graph_nodes(payload: GraphSearchRequest) -> dict[str, Any]:
    """Filters system graph nodes by type, domain, provenance, or name substring."""
    topology = orchestrator.get_system_graph()
    results = list(topology.nodes)

    # Filter by node_type
    if payload.node_type:
        try:
            nt = GraphNodeType(payload.node_type.upper())
            results = [n for n in results if n.node_type == nt]
        except ValueError as err:
            valid_vals = [t.value for t in GraphNodeType]
            raise HTTPException(
                status_code=400,
                detail=f"Invalid node_type '{payload.node_type}'. Valid values: {valid_vals}",
            ) from err

    # Filter by domain
    if payload.domain:
        try:
            dom = GraphDomainType(payload.domain.upper())
            results = [n for n in results if n.domain == dom]
        except ValueError as err:
            valid_vals = [d.value for d in GraphDomainType]
            raise HTTPException(
                status_code=400,
                detail=f"Invalid domain '{payload.domain}'. Valid values: {valid_vals}",
            ) from err

    # Filter by provenance
    if payload.provenance:
        try:
            prov = ProvenanceState(payload.provenance.upper())
            results = [n for n in results if n.provenance == prov]
        except ValueError as err:
            valid_vals = [p.value for p in ProvenanceState]
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provenance '{payload.provenance}'. Valid values: {valid_vals}",
            ) from err

    # Filter by name substring
    if payload.name_contains:
        results = [n for n in results if payload.name_contains.lower() in n.name.lower()]

    return {
        "matched_count": len(results),
        "filters": payload.model_dump(exclude_none=True),
        "nodes": [_node_to_dict(n) for n in results],
    }


@router.post("/graph/rebuild")
async def rebuild_system_graph() -> dict[str, Any]:
    """Force-rebuilds the system graph topology and returns summary with timing."""
    start = time.perf_counter()
    topology = orchestrator.graph_builder.build_full_system_graph()
    elapsed_ms = round((time.perf_counter() - start) * 1000.0, 2)

    return {
        "status": "REBUILT",
        "twin_id": topology.twin_id,
        "total_nodes": topology.total_nodes,
        "total_edges": topology.total_edges,
        "provenance_summary": topology.provenance_summary,
        "rebuild_duration_ms": elapsed_ms,
        "timestamp": topology.timestamp,
    }


@router.post("/impact")
async def analyze_target_impact(payload: ImpactAnalysisRequest) -> dict[str, Any]:
    """Computes systemic blast radius and affected capabilities for target file/module."""
    if not payload.target_file.strip():
        raise HTTPException(status_code=400, detail="target_file parameter must not be empty")

    report = orchestrator.analyze_file_impact(payload.target_file)
    return _impact_to_dict(report)


@router.get("/consistency")
async def audit_graph_consistency() -> dict[str, Any]:
    """Audits topology for clean architecture violations and stale runtime mappings."""
    report = orchestrator.audit_graph_consistency()
    return _consistency_to_dict(report)


@router.post("/delta")
async def compare_graph_delta(payload: DeltaComparisonRequest) -> dict[str, Any]:
    """Compares current system graph topology against a saved snapshot."""
    report = orchestrator.delta_checkpoint.compare_delta(
        before_snapshot_name=payload.before_snapshot_name,
        after_topology=orchestrator.get_system_graph(),
        max_allowed_node_delta=payload.max_allowed_node_delta,
    )
    return _delta_to_dict(report)


@router.get("/snapshots")
async def list_graph_snapshots() -> dict[str, Any]:
    """Lists all saved topology snapshots with their names and timestamps."""
    snapshots = orchestrator.delta_checkpoint.list_snapshots()
    return {
        "total_snapshots": len(snapshots),
        "snapshots": snapshots,
    }


@router.post("/snapshots/save")
async def save_graph_snapshot(payload: SnapshotSaveRequest) -> dict[str, Any]:
    """Saves current system graph topology as a named snapshot."""
    if not payload.snapshot_name.strip():
        raise HTTPException(status_code=400, detail="snapshot_name must not be empty")

    topology = orchestrator.get_system_graph()
    name = orchestrator.delta_checkpoint.capture_snapshot(payload.snapshot_name, topology)

    return {
        "status": "SAVED",
        "snapshot_name": name,
        "total_nodes": topology.total_nodes,
        "total_edges": topology.total_edges,
        "timestamp": topology.timestamp,
    }


@router.delete("/snapshots/{snapshot_name}")
async def delete_graph_snapshot(snapshot_name: str) -> dict[str, Any]:
    """Deletes a saved topology snapshot."""
    deleted = orchestrator.delta_checkpoint.delete_snapshot(snapshot_name)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Snapshot '{snapshot_name}' not found")

    return {"status": "DELETED", "snapshot_name": snapshot_name}


@router.post("/simulate")
async def simulate_scenario(payload: SimulationRequest) -> dict[str, Any]:
    """Runs a what-if simulation scenario on the current Digital Twin state."""
    result = orchestrator.simulate_change(payload.scenario_name)
    return result.model_dump()


@router.get("/state")
async def get_twin_state() -> dict[str, Any]:
    """Returns current Digital Twin aggregate state snapshot."""
    state = orchestrator.get_current_twin_state()
    return state.model_dump(mode="json")
