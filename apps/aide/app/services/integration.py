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

MISSING_GATEWAY_CONTRACTS: Final[tuple[GatewayContract, ...]] = (
    GatewayContract(
        name="task-status",
        method="GET",
        path="/tasks/{task_id}",
        state="missing",
        purpose="No discovered task status route in current Gateway routers.",
    ),
    GatewayContract(
        name="lifecycle-event-stream",
        method="WEBSOCKET",
        path="/ws/chat or lifecycle stream",
        state="missing",
        purpose="No discovered WebSocket route in current apps/api checkout.",
    ),
)


def list_gateway_contracts() -> list[GatewayContract]:
    """Return real and missing Gateway contracts used by AIDE."""

    return [*REAL_GATEWAY_CONTRACTS, *MISSING_GATEWAY_CONTRACTS]


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
    results.extend(
        GatewayResult(
            contract=contract.name,
            target=contract.path,
            status="missing",
            detail=contract.purpose,
        )
        for contract in MISSING_GATEWAY_CONTRACTS
    )
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
