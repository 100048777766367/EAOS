"""Canonical System Graph Data Models & Provenance Specifications for EAOS Digital Twin."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class GraphDomainType(StrEnum):
    """The 8 Core System Graph Node Domains."""

    ARCHITECTURE = "ARCHITECTURE"
    SOURCE = "SOURCE"
    DEPENDENCY = "DEPENDENCY"
    RUNTIME = "RUNTIME"
    BEHAVIOR = "BEHAVIOR"
    SECURITY = "SECURITY"
    GOVERNANCE = "GOVERNANCE"
    MEMORY = "MEMORY"


class GraphNodeType(StrEnum):
    """Canonical Node Types in EAOS System Graph."""

    BOUNDED_CONTEXT = "BOUNDED_CONTEXT"
    LAYER = "LAYER"
    PORT = "PORT"
    ADAPTER = "ADAPTER"
    APPLICATION = "APPLICATION"
    PACKAGE = "PACKAGE"
    MODULE = "MODULE"
    CLASS = "CLASS"
    FUNCTION = "FUNCTION"
    INTERFACE = "INTERFACE"
    SERVICE = "SERVICE"
    PROCESS = "PROCESS"
    ENDPOINT_API = "ENDPOINT_API"
    ENDPOINT_WEBSOCKET = "ENDPOINT_WEBSOCKET"
    AGENT = "AGENT"
    TASK = "TASK"
    TEST = "TEST"
    INVARIANT = "INVARIANT"
    POLICY = "POLICY"
    SECURITY_BOUNDARY = "SECURITY_BOUNDARY"
    DECISION_ADR = "DECISION_ADR"
    FAILURE_RECORD = "FAILURE_RECORD"


class GraphEdgeType(StrEnum):
    """Typed Directed Relationship Edges."""

    IMPORTS = "IMPORTS"
    IMPLEMENTS = "IMPLEMENTS"
    DEPENDS_ON = "DEPENDS_ON"
    IMPLEMENTED_BY = "IMPLEMENTED_BY"
    CONNECTS_TO = "CONNECTS_TO"
    EXPOSES = "EXPOSES"
    HANDLES = "HANDLES"
    CONNECTS = "CONNECTS"
    EXECUTES = "EXECUTES"
    MUTATES = "MUTATES"
    VERIFIED_BY = "VERIFIED_BY"
    PROTECTS = "PROTECTS"
    GOVERNED_BY = "GOVERNED_BY"
    AUTHORIZED_BY = "AUTHORIZED_BY"


class ProvenanceState(StrEnum):
    """Provenance & Trust State of Graph Entity or Relationship."""

    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    DECLARED = "DECLARED"
    VERIFIED = "VERIFIED"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"


class BlastRadiusCategory(StrEnum):
    """Blast Radius Impact Risk Classification."""

    LOCAL = "LOCAL"
    SMALL = "SMALL"
    BROAD = "BROAD"
    MASS = "MASS"
    SYSTEMIC = "SYSTEMIC"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class GraphNodeDTO:
    """Canonical representation of a single Node in the System Graph."""

    node_id: str
    name: str
    domain: GraphDomainType
    node_type: GraphNodeType
    provenance: ProvenanceState
    source_of_truth: str
    authority_level: str = "L0"
    last_observed: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GraphEdgeDTO:
    """Canonical representation of a directed Edge in the System Graph."""

    source_node_id: str
    target_node_id: str
    edge_type: GraphEdgeType
    provenance: ProvenanceState
    evidence_ref: str = ""
    last_observed: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SystemGraphTopologyDTO:
    """Complete snapshot representation of EAOS System Graph Topology."""

    twin_id: str
    total_nodes: int
    total_edges: int
    provenance_summary: dict[str, int]
    nodes: list[GraphNodeDTO]
    edges: list[GraphEdgeDTO]
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
