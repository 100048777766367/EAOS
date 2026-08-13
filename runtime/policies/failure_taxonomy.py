"""Runtime Failure Taxonomy & Failure Classifier for EAOS Runtime Control Plane."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class RuntimeFailureCategory(StrEnum):
    """Canonical Taxonomy of Runtime Failures in EAOS."""

    CONFIGURATION_FAILURE = "CONFIGURATION_FAILURE"
    STARTUP_FAILURE = "STARTUP_FAILURE"
    CONNECTION_FAILURE = "CONNECTION_FAILURE"
    PROCESS_FAILURE = "PROCESS_FAILURE"
    AGENT_FAILURE = "AGENT_FAILURE"
    TOOL_FAILURE = "TOOL_FAILURE"
    APPLICATION_FAILURE = "APPLICATION_FAILURE"
    CONTRACT_FAILURE = "CONTRACT_FAILURE"
    SECURITY_BLOCK = "SECURITY_BLOCK"
    UNKNOWN_FAILURE = "UNKNOWN_FAILURE"


@dataclass(frozen=True)
class RuntimeFailureRecord:
    """Immutable record of an observed runtime failure."""

    failure_id: str
    category: RuntimeFailureCategory
    symptom: str
    root_cause: str
    affected_component: str
    task_id: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    details: dict[str, Any] = field(default_factory=dict)


class RuntimeFailureClassifier:
    """Classifies exceptions, log signals, and diagnostics into canonical RuntimeFailureCategory."""

    @staticmethod
    def classify_exception(
        exc: Exception | str,
        affected_component: str = "runtime",
        task_id: str | None = None,
    ) -> RuntimeFailureRecord:
        """Classifies python exception or error message string."""
        err_msg = str(exc)
        err_type = exc.__class__.__name__ if isinstance(exc, Exception) else "StringError"

        # Classification heuristic rules
        if (
            "PermissionError" in err_type
            or "Security" in err_type
            or "Forbidden" in err_msg
            or "PathTraversal" in err_msg
        ):
            cat = RuntimeFailureCategory.SECURITY_BLOCK
        elif (
            "ConnectionRefusedError" in err_type
            or "WebSocketDisconnect" in err_type
            or "socket" in err_msg.lower()
            or "connect" in err_msg.lower()
        ):
            cat = RuntimeFailureCategory.CONNECTION_FAILURE
        elif "ValidationError" in err_type or "JSONDecodeError" in err_type or "schema" in err_msg.lower():
            cat = RuntimeFailureCategory.CONTRACT_FAILURE
        elif "ImportError" in err_type or "ModuleNotFoundError" in err_type or "lifespan" in err_msg.lower():
            cat = RuntimeFailureCategory.STARTUP_FAILURE
        elif "KeyError" in err_type or "ValueError" in err_type or "Config" in err_msg or "Settings" in err_msg:
            cat = RuntimeFailureCategory.CONFIGURATION_FAILURE
        elif "SubprocessError" in err_type or "Tool" in err_type or "cmd" in err_msg.lower():
            cat = RuntimeFailureCategory.TOOL_FAILURE
        elif "Agent" in err_type or "orchestrator" in err_msg.lower():
            cat = RuntimeFailureCategory.AGENT_FAILURE
        elif "Process" in err_type or "pid" in err_msg.lower():
            cat = RuntimeFailureCategory.PROCESS_FAILURE
        else:
            cat = RuntimeFailureCategory.APPLICATION_FAILURE

        import uuid

        return RuntimeFailureRecord(
            failure_id=f"fail-{uuid.uuid4().hex[:8]}",
            category=cat,
            symptom=f"{err_type}: {err_msg[:120]}",
            root_cause=f"{cat.value} detected in {affected_component}",
            affected_component=affected_component,
            task_id=task_id,
            details={"error_type": err_type, "error_full": err_msg},
        )
