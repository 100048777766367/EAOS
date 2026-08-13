"""System Graph Builder Engine parsing AST imports, source files, and live runtime state."""

from __future__ import annotations

import ast
import uuid
from pathlib import Path

from digitaltwin.models.canonical_graph_model import (
    GraphDomainType,
    GraphEdgeDTO,
    GraphEdgeType,
    GraphNodeDTO,
    GraphNodeType,
    ProvenanceState,
    SystemGraphTopologyDTO,
)
from runtime.runtime_control_plane import RuntimeControlPlane


class SystemGraphBuilder:
    """Scans repository code AST and runtime state to construct the canonical System Graph."""

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()
        self.nodes: dict[str, GraphNodeDTO] = {}
        self.edges: list[GraphEdgeDTO] = []
        self.runtime_plane = RuntimeControlPlane()

    def build_full_system_graph(self) -> SystemGraphTopologyDTO:
        """Executes full repository AST scan and runtime state integration."""
        self.nodes.clear()
        self.edges.clear()

        # 1. Scan Source Files & AST Dependencies
        self._scan_source_files()

        # 2. Integrate Task 3 Runtime Control Plane State
        self._integrate_runtime_state()

        # 3. Integrate Governance & Architecture Policy Nodes
        self._integrate_governance_nodes()

        # Calculate Provenance Summary
        provenance_counts: dict[str, int] = {}
        for n in self.nodes.values():
            provenance_counts[n.provenance.value] = provenance_counts.get(n.provenance.value, 0) + 1

        return SystemGraphTopologyDTO(
            twin_id=f"dtwin-{uuid.uuid4().hex[:8]}",
            total_nodes=len(self.nodes),
            total_edges=len(self.edges),
            provenance_summary=provenance_counts,
            nodes=list(self.nodes.values()),
            edges=list(self.edges),
        )

    def _scan_source_files(self) -> None:
        """Scans Python modules in core directories for AST imports & structural nodes."""
        target_dirs = ["apps", "packages", "runtime", "platforms", "engine", "kernel", "tools"]

        for dir_name in target_dirs:
            dir_path = self.root_path / dir_name
            if not dir_path.exists():
                continue

            for py_file in dir_path.rglob("*.py"):
                if "__pycache__" in py_file.parts or ".venv" in py_file.parts:
                    continue

                rel_path = py_file.relative_to(self.root_path).as_posix()
                node_id = f"mod:{rel_path}"

                # Determine Domain & Layer
                domain = GraphDomainType.SOURCE
                node_type = GraphNodeType.MODULE
                if "domain" in py_file.parts:
                    domain = GraphDomainType.ARCHITECTURE
                    node_type = GraphNodeType.BOUNDED_CONTEXT
                elif "infrastructure" in py_file.parts or "adapters" in py_file.parts:
                    domain = GraphDomainType.ARCHITECTURE
                    node_type = GraphNodeType.ADAPTER
                elif "ports" in py_file.parts:
                    domain = GraphDomainType.ARCHITECTURE
                    node_type = GraphNodeType.PORT

                self.nodes[node_id] = GraphNodeDTO(
                    node_id=node_id,
                    name=py_file.name,
                    domain=domain,
                    node_type=node_type,
                    provenance=ProvenanceState.VERIFIED,
                    source_of_truth=rel_path,
                )

                # AST Import Parsing
                self._parse_file_ast_imports(py_file, node_id)

    def _parse_file_ast_imports(self, file_path: Path, source_node_id: str) -> None:
        """Extracts AST imports from a single file and creates IMPORTS edges."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(content, filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._add_import_edge(source_node_id, alias.name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    self._add_import_edge(source_node_id, node.module)
        except Exception:
            pass

    def _add_import_edge(self, source_node_id: str, imported_module_path: str) -> None:
        """Resolves imported module string to graph node and adds edge."""
        clean_path = imported_module_path.replace(".", "/")
        target_node_id = f"mod:{clean_path}.py"

        # Add edge even if target node is inferred
        self.edges.append(
            GraphEdgeDTO(
                source_node_id=source_node_id,
                target_node_id=target_node_id,
                edge_type=GraphEdgeType.IMPORTS,
                provenance=ProvenanceState.OBSERVED,
                evidence_ref="AST_Parser",
            )
        )

    def _integrate_runtime_state(self) -> None:
        """Attaches live process PIDs and HTTP/WS routes from RuntimeControlPlane."""
        status = self.runtime_plane.get_control_status()

        # Add Runtime Processes as Graph Nodes
        for proc in status.processes:
            proc_node_id = f"proc:{proc.capability_name}"
            prov = ProvenanceState.VERIFIED if proc.state.value == "HEALTHY" else ProvenanceState.STALE

            self.nodes[proc_node_id] = GraphNodeDTO(
                node_id=proc_node_id,
                name=proc.capability_name,
                domain=GraphDomainType.RUNTIME,
                node_type=GraphNodeType.PROCESS,
                provenance=prov,
                source_of_truth=f"{proc.expected_host}:{proc.expected_port}",
                metadata={"pid": proc.pid, "state": proc.state.value},
            )

        # Add API & WebSocket Gateway Endpoints
        api_ep_id = "ep:api_gateway_8000"
        ws_ep_id = "ep:ws_chat_8000"

        self.nodes[api_ep_id] = GraphNodeDTO(
            node_id=api_ep_id,
            name="FastAPI Gateway (HTTP 8000)",
            domain=GraphDomainType.RUNTIME,
            node_type=GraphNodeType.ENDPOINT_API,
            provenance=ProvenanceState.VERIFIED,
            source_of_truth="apps/api/app/main.py",
        )

        self.nodes[ws_ep_id] = GraphNodeDTO(
            node_id=ws_ep_id,
            name="Chat Stream (WS /ws/chat)",
            domain=GraphDomainType.RUNTIME,
            node_type=GraphNodeType.ENDPOINT_WEBSOCKET,
            provenance=ProvenanceState.VERIFIED,
            source_of_truth="apps/api/app/routers/chat.py",
        )

        # Connect API -> Process
        self.edges.append(
            GraphEdgeDTO(
                source_node_id=api_ep_id,
                target_node_id="proc:api_gateway",
                edge_type=GraphEdgeType.EXPOSES,
                provenance=ProvenanceState.VERIFIED,
                evidence_ref="RuntimeControlPlane",
            )
        )

    def _integrate_governance_nodes(self) -> None:
        """Adds Constitutional governance nodes and hard invariants."""
        gov_node_id = "gov:ARCHITECTURE_CONSTITUTION"
        self.nodes[gov_node_id] = GraphNodeDTO(
            node_id=gov_node_id,
            name="ARCHITECTURE_CONSTITUTION.md",
            domain=GraphDomainType.GOVERNANCE,
            node_type=GraphNodeType.POLICY,
            provenance=ProvenanceState.DECLARED,
            source_of_truth="ARCHITECTURE_CONSTITUTION.md",
            authority_level="L7",
        )
