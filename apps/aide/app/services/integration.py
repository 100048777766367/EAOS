"""AIDE integration orchestration against existing Gateway contracts."""

from typing import Any, Final

from apps.aide.app.adapters.gateway_client import request_gateway_json
from apps.aide.app.schemas.gateway import GatewayContract, GatewayResult
from apps.aide.app.settings import AideSettings

REAL_GATEWAY_CONTRACTS: Final[tuple[GatewayContract, ...]] = (
    GatewayContract(
        name="health",
        method="GET",
        path="/health",
        purpose="Gateway health observation.",
    ),
    GatewayContract(
        name="task-submission",
        method="POST",
        path="/api/v1/control/execute",
        purpose="Submit governed engineering command to Gateway control route.",
    ),
    GatewayContract(
        name="runtime-state",
        method="GET",
        path="/v1/capabilities",
        purpose="Observe Gateway-exposed runtime capability registry.",
    ),
    GatewayContract(
        name="governance-state",
        method="POST",
        path="/governance/opa/evaluate",
        purpose="Ask Gateway governance policy evaluator for an observed result.",
    ),
    GatewayContract(
        name="evidence-result",
        method="POST",
        path="/governance/ledger/verify-merkle",
        purpose="Ask Gateway evidence ledger verifier for Merkle proof state.",
    ),
)

TASK_LIFECYCLE_CONTRACTS: Final[tuple[GatewayContract, ...]] = (
    GatewayContract(
        name="task-status",
        method="GET",
        path="/api/v1/tasks/{task_id}",
        purpose="Observe real Gateway task lifecycle state.",
    ),
    GatewayContract(
        name="lifecycle-event-stream",
        method="WEBSOCKET",
        path="/api/v1/tasks/{task_id}/events",
        purpose="Consume Gateway task lifecycle events.",
    ),
)

MISSING_GATEWAY_CONTRACTS: Final[tuple[GatewayContract, ...]] = ()


def list_gateway_contracts() -> list[GatewayContract]:
    """Return real and missing Gateway contracts used by AIDE."""

    return [*REAL_GATEWAY_CONTRACTS, *TASK_LIFECYCLE_CONTRACTS]


async def build_gateway_snapshot(settings: AideSettings) -> list[GatewayResult]:
    """Observe read-side Gateway state and document missing contracts."""

    results: list[GatewayResult] = []
    probes = [
        ("health", "GET", "/health", None),
        ("runtime-state", "GET", "/v1/capabilities", None),
        ("evidence-result", "POST", "/governance/ledger/verify-merkle", {}),
    ]
    for contract, method, path, payload in probes:
        observed = await request_gateway_json(
            settings,
            contract,
            method,
            path,
            payload,
        )
        results.append(observed)
    return results


async def submit_task(
    settings: AideSettings,
    command: str,
    target_agent: str = "planner",
) -> GatewayResult:
    """Submit an engineering command through the existing Gateway route."""

    payload: dict[str, Any] = {"command": command, "target_agent": target_agent}
    return await request_gateway_json(
        settings,
        "task-submission",
        "POST",
        "/api/v1/control/execute",
        payload,
    )


async def get_task_status(settings: AideSettings, task_id: str) -> GatewayResult:
    """Read task lifecycle status from the Gateway."""

    return await request_gateway_json(
        settings,
        "task-status",
        "GET",
        f"/api/v1/tasks/{task_id}",
    )


async def get_capability_registry(settings: AideSettings) -> GatewayResult:
    """Read the authoritative Gateway capability contract registry."""

    return await request_gateway_json(
        settings,
        "capability-registry",
        "GET",
        "/v1/capabilities",
    )
