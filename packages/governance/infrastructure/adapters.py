"""Infrastructure Adapters for Governance Capability with Neo4j & Persistence."""

import base64
import json
import threading
import urllib.request
from pathlib import Path
from typing import Any

from packages.governance.domain.ports import (
    AuditSnapshotDTO,
    GovernancePolicyProviderPort,
    GovernanceRepositoryPort,
    KnowledgeGraphPort,
    TopologyScanDTO,
    TopologyScannerPort,
)
from packages.governance.infrastructure.scanner_components import (
    ASTSafeParser,
    WorkspaceWalker,
)


class ComponentizedTopologyScannerAdapter(TopologyScannerPort):
    """Scanner Adapter delegating tasks to SRP sub-components."""

    def __init__(self, root_dir: Path) -> None:
        self.walker = WorkspaceWalker(root_dir)
        self.parser = ASTSafeParser()

    def scan_topology(self) -> TopologyScanDTO:
        return self.scan_workspace()

    def scan_workspace(self) -> TopologyScanDTO:
        py_files, empty_dirs = self.walker.walk()
        all_imports: list[tuple[str, str]] = []
        diagnostics = []

        for f_path in py_files:
            imports, diag = self.parser.parse_file(f_path)
            all_imports.extend(imports)
            if diag:
                diagnostics.append(diag)

        return TopologyScanDTO(
            active_py_files=len(py_files),
            empty_directories=empty_dirs,
            import_records=all_imports,
            diagnostics=diagnostics,
        )


class YamlGovernancePolicyAdapter(GovernancePolicyProviderPort):
    """Adapter loading governance policy rules from YAML configuration."""

    def __init__(self, policy_path: Path) -> None:
        self.policy_path: Path = policy_path

    def get_policies(self) -> list[dict[str, Any]]:
        res = self.load_policy()
        return [res] if isinstance(res, dict) else []

    def load_policy(self) -> dict[str, Any]:
        if not self.policy_path.exists():
            return {
                "base_health_score": 100.0,
                "fitness_rules": {
                    "hexagonal_boundary": {"penalty_per_violation": 10.0},
                    "empty_directory": {"penalty_per_directory": 2.0},
                },
            }

        try:
            import yaml

            content = self.policy_path.read_text(encoding="utf-8")
            parsed = yaml.safe_load(content)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {
                "base_health_score": 100.0,
                "fitness_rules": {
                    "hexagonal_boundary": {"penalty_per_violation": 10.0},
                    "empty_directory": {"penalty_per_directory": 2.0},
                },
            }


class PersistentJsonSnapshotRepositoryAdapter(GovernanceRepositoryPort):
    """Persistent Repository storing snapshots with thread-safe file locking."""

    def __init__(self, ledger_path: Path) -> None:
        self.ledger_path: Path = ledger_path
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def save_snapshot(self, snapshot: AuditSnapshotDTO) -> None:
        with self._lock, open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(snapshot.model_dump_json() + "\n")

    def get_latest_snapshot(self) -> AuditSnapshotDTO | None:
        history = self.get_snapshot_history()
        return history[-1] if history else None

    def get_snapshot_history(self) -> list[AuditSnapshotDTO]:
        if not self.ledger_path.exists():
            return []
        snapshots = []
        with self._lock, open(self.ledger_path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        snapshots.append(AuditSnapshotDTO(**data))
                    except Exception:
                        pass
        return snapshots

    def count_records(self) -> int:
        """Thực thi phương thức đếm số lượng bản ghi snapshot trong ledger."""
        return len(self.get_snapshot_history())


class Neo4jRestAdapter(KnowledgeGraphPort):
    """Adapter querying live Neo4j Knowledge Graph via REST API."""

    def __init__(
        self,
        url: str = "http://localhost:7474/db/neo4j/tx/commit",
        auth: tuple[str, str] = ("neo4j", "password"),
    ) -> None:
        self.url = url
        self.auth = auth

    def query_graph(self, query: str) -> dict[str, Any]:
        return {}

    def query_system_node_count(self) -> int:
        """Đưa logic truy vấn từ __init__ về đúng phương thức này."""
        try:
            auth_str = f"{self.auth[0]}:{self.auth[1]}"
            b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            payload = json.dumps({"statements": [{"statement": "MATCH (n) RETURN count(n) AS c"}]}).encode("utf-8")

            req = urllib.request.Request(
                self.url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {b64_auth}",
                },
            )
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    results = data.get("results", [])
                    if results and results[0].get("data"):
                        row = results[0]["data"][0].get("row", [0])
                        return int(row[0])
        except Exception:
            pass
        return 0
