"""Process Control & Process Ownership Manager for EAOS Runtime Control Plane."""

from __future__ import annotations

import os
import socket
import subprocess
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import ClassVar


class ProcessState(StrEnum):
    """Process & Socket status classifications."""

    HEALTHY = "HEALTHY"
    MISSING = "MISSING"
    CRASHED = "CRASHED"
    WRONG_PORT = "WRONG_PORT"
    DUPLICATE = "DUPLICATE"
    STALE = "STALE"
    INACCESSIBLE = "INACCESSIBLE"


@dataclass(frozen=True)
class ProcessOwnershipDTO:
    """Ownership mapping between capability, process, host, and port."""

    capability_name: str
    service_name: str
    expected_host: str
    expected_port: int
    pid: int | None = None
    state: ProcessState = ProcessState.MISSING
    last_inspected: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    details: str = ""


class ProcessManager:
    """Discovers, tracks, and verifies process ownership for EAOS runtime capabilities."""

    DEFAULT_PORT_MAPPINGS: ClassVar[dict[str, tuple[str, int]]] = {
        "api_gateway": ("127.0.0.1", 8000),
        "web_ui": ("127.0.0.1", 3002),
        "neo4j_db": ("127.0.0.1", 7474),
        "prometheus_metrics": ("127.0.0.1", 9090),
        "ollama_llm": ("127.0.0.1", 11434),
    }

    def __init__(self) -> None:
        self._registered_owners: dict[str, ProcessOwnershipDTO] = {}
        self._init_defaults()

    def _init_defaults(self) -> None:
        for cap, (host, port) in self.DEFAULT_PORT_MAPPINGS.items():
            self._registered_owners[cap] = ProcessOwnershipDTO(
                capability_name=cap,
                service_name=f"service-{cap}",
                expected_host=host,
                expected_port=port,
                state=ProcessState.MISSING,
                details="Uninitialized probe",
            )

    @staticmethod
    def is_port_listening(host: str, port: int, timeout_sec: float = 0.5) -> bool:
        """Safe TCP socket probe to verify active listener on host:port."""
        try:
            with socket.create_connection((host, port), timeout=timeout_sec):
                return True
        except OSError:
            return False

    def inspect_capability_process(self, capability_name: str) -> ProcessOwnershipDTO:
        """Audits the actual process state of a capability."""
        ownership = self._registered_owners.get(capability_name)
        if not ownership:
            return ProcessOwnershipDTO(
                capability_name=capability_name,
                service_name=f"service-{capability_name}",
                expected_host="127.0.0.1",
                expected_port=0,
                state=ProcessState.MISSING,
                details="Capability not registered in ProcessManager",
            )

        # Check socket listening
        host = ownership.expected_host
        port = ownership.expected_port
        is_listening = self.is_port_listening(host, port)

        if is_listening:
            pid = self._find_pid_for_port(port)
            updated = ProcessOwnershipDTO(
                capability_name=capability_name,
                service_name=ownership.service_name,
                expected_host=host,
                expected_port=port,
                pid=pid,
                state=ProcessState.HEALTHY,
                details=f"Port {port} actively listening (PID: {pid})",
            )
        else:
            if ownership.pid and self._is_pid_running(ownership.pid):
                updated = ProcessOwnershipDTO(
                    capability_name=capability_name,
                    service_name=ownership.service_name,
                    expected_host=host,
                    expected_port=port,
                    pid=ownership.pid,
                    state=ProcessState.WRONG_PORT,
                    details=f"PID {ownership.pid} running but port {port} not listening",
                )
            else:
                updated = ProcessOwnershipDTO(
                    capability_name=capability_name,
                    service_name=ownership.service_name,
                    expected_host=host,
                    expected_port=port,
                    pid=None,
                    state=ProcessState.MISSING,
                    details=f"Port {port} is not listening",
                )

        self._registered_owners[capability_name] = updated
        return updated

    def inspect_all_processes(self) -> list[ProcessOwnershipDTO]:
        """Audits all registered capability processes."""
        return [self.inspect_capability_process(cap) for cap in list(self._registered_owners.keys())]

    def _find_pid_for_port(self, port: int) -> int | None:
        """Safe subprocess call to discover PID listening on specified port."""
        if os.name != "nt":
            return None

        try:
            cmd = ["cmd.exe", "/c", f"netstat -ano | findstr :{port}"]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
            if res.returncode == 0 and res.stdout:
                lines = res.stdout.strip().splitlines()
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 5 and "LISTENING" in parts:
                        return int(parts[-1])
        except Exception:
            pass
        return None

    def _is_pid_running(self, pid: int) -> bool:
        """Verifies if PID exists and is active."""
        if os.name != "nt":
            return False
        try:
            cmd = ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV"]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
            return str(pid) in res.stdout
        except Exception:
            return False
