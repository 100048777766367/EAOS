"""Authoritative Gateway capability contract discovery registry."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

CapabilityStatus = Literal["available", "degraded", "unavailable", "contract_gap"]
CapabilityTransport = Literal["http", "websocket", "internal"]
CapabilityOperation = Literal["read", "write", "execute", "events", "observe"]


class CapabilityEndpoint(BaseModel):
    """Discovery metadata for an existing Gateway endpoint."""

    model_config = ConfigDict(frozen=True)

    method: str
    path: str
    transport: CapabilityTransport = "http"


class GatewayCapabilityContract(BaseModel):
    """Discovery-only metadata for an EAOS capability contract."""

    model_config = ConfigDict(frozen=True)

    capability_id: str
    name: str
    version: str = "1"
    owner: str
    status: CapabilityStatus
    description: str
    transport: tuple[CapabilityTransport, ...]
    endpoints: tuple[CapabilityEndpoint, ...] = Field(default_factory=tuple)
    operations: tuple[CapabilityOperation, ...] = Field(default_factory=tuple)
    evidence_supported: bool = False
    governance_supported: bool = False
    verification_supported: bool = False
    correlation_supported: bool = False
    dependencies: tuple[str, ...] = Field(default_factory=tuple)
    metadata: dict[str, Any] = Field(default_factory=dict)


CAPABILITY_CONTRACTS: tuple[GatewayCapabilityContract, ...] = (
    GatewayCapabilityContract(
        capability_id="gateway.health",
        name="Gateway Health",
        owner="apps.api.routers.health",
        status="available",
        description="Observed API Gateway process health contract.",
        transport=("http",),
        endpoints=(CapabilityEndpoint(method="GET", path="/health"),),
        operations=("observe", "read"),
    ),
    GatewayCapabilityContract(
        capability_id="capability.discovery",
        name="Capability Discovery",
        owner="apps.api.routers.capability_runtime",
        status="available",
        description="Explicit Gateway registry of existing EAOS capability contracts and gaps.",
        transport=("http",),
        endpoints=(CapabilityEndpoint(method="GET", path="/v1/capabilities"),),
        operations=("read",),
    ),
    GatewayCapabilityContract(
        capability_id="task.lifecycle",
        name="Task Lifecycle",
        owner="apps.api.task_lifecycle",
        status="available",
        description="Gateway-owned governed task submission, status, lifecycle events, and terminal states.",
        transport=("http", "websocket"),
        endpoints=(
            CapabilityEndpoint(method="POST", path="/api/v1/control/execute"),
            CapabilityEndpoint(method="GET", path="/api/v1/tasks/{task_id}"),
            CapabilityEndpoint(method="WEBSOCKET", path="/api/v1/tasks/{task_id}/events", transport="websocket"),
        ),
        operations=("execute", "read", "events"),
        evidence_supported=True,
        governance_supported=True,
        verification_supported=True,
        correlation_supported=True,
        dependencies=("governance.policy",),
        metadata={
            "lifecycle_states": ["accepted", "planning", "executing", "verifying", "completed", "failed", "denied"]
        },
    ),
    GatewayCapabilityContract(
        capability_id="governance.policy",
        name="Governance Policy Evaluation",
        owner="apps.api.routers.governance",
        status="available",
        description="Gateway governance and policy evaluation contracts.",
        transport=("http",),
        endpoints=(
            CapabilityEndpoint(method="POST", path="/governance/opa/evaluate"),
            CapabilityEndpoint(method="POST", path="/governance/rego/compile-eval"),
        ),
        operations=("execute", "read"),
        governance_supported=True,
        correlation_supported=False,
    ),
    GatewayCapabilityContract(
        capability_id="evidence.ledger",
        name="Evidence Ledger Verification",
        owner="apps.api.routers.governance",
        status="available",
        description="Gateway contract for ledger/Merkle evidence verification.",
        transport=("http",),
        endpoints=(CapabilityEndpoint(method="POST", path="/governance/ledger/verify-merkle"),),
        operations=("read", "execute"),
        evidence_supported=True,
        verification_supported=True,
    ),
    GatewayCapabilityContract(
        capability_id="memory.knowledge",
        name="Memory and Knowledge Search",
        owner="apps.api.routers.memory_knowledge",
        status="available",
        description="Gateway contracts for memory listing/storage and hybrid knowledge search.",
        transport=("http",),
        endpoints=(
            CapabilityEndpoint(method="GET", path="/v1/memory"),
            CapabilityEndpoint(method="POST", path="/v1/memory/store"),
            CapabilityEndpoint(method="POST", path="/memory/hybrid-search"),
        ),
        operations=("read", "write"),
        evidence_supported=True,
        correlation_supported=False,
    ),
    GatewayCapabilityContract(
        capability_id="telemetry.observation",
        name="Telemetry Observation",
        owner="apps.api.routers.telemetry_performance",
        status="available",
        description="Gateway telemetry ingest, OTLP export, and telemetry-fitness evaluation contracts.",
        transport=("http",),
        endpoints=(
            CapabilityEndpoint(method="POST", path="/telemetry/ingest"),
            CapabilityEndpoint(method="POST", path="/telemetry/otlp/export-span"),
            CapabilityEndpoint(method="POST", path="/telemetry/fitness-bridge/eval"),
        ),
        operations=("write", "execute"),
        verification_supported=True,
    ),
    GatewayCapabilityContract(
        capability_id="runtime.sandbox",
        name="Runtime Sandbox Execution",
        owner="apps.api.routers.resilience",
        status="available",
        description="Existing Gateway sandbox execution contract; AIDE must not call it as a local execution path.",
        transport=("http",),
        endpoints=(CapabilityEndpoint(method="POST", path="/sandbox/wasm/execute"),),
        operations=("execute",),
        verification_supported=True,
        metadata={"aide_exposure": "not_exposed"},
    ),
    GatewayCapabilityContract(
        capability_id="orchestration.autonomous",
        name="Autonomous Orchestration",
        owner="apps.api.routers.autonomous",
        status="available",
        description="Existing autonomous loop contract owned by the Gateway and packages/autonomous.",
        transport=("http",),
        endpoints=(CapabilityEndpoint(method="POST", path="/autonomous/run-cycle"),),
        operations=("execute",),
        governance_supported=True,
        verification_supported=True,
        metadata={"aide_exposure": "not_exposed"},
    ),
    GatewayCapabilityContract(
        capability_id="security.controls",
        name="Security Controls",
        owner="apps.api.routers.security",
        status="available",
        description="Existing Gateway security controls; AIDE has no direct control UI in this phase.",
        transport=("http",),
        endpoints=(),
        operations=("read",),
        governance_supported=True,
        metadata={"aide_exposure": "not_exposed"},
    ),
    GatewayCapabilityContract(
        capability_id="federation.registry",
        name="Federation Registry",
        owner="apps.api.routers.federation",
        status="available",
        description="Existing Gateway federation router and registry-backed contracts.",
        transport=("http",),
        endpoints=(),
        operations=("read", "write"),
        metadata={"aide_exposure": "not_exposed"},
    ),
    GatewayCapabilityContract(
        capability_id="tenancy.registry",
        name="Tenancy Registry",
        owner="apps.api.routers.tenancy",
        status="available",
        description="Existing Gateway tenancy router and tenant registry-backed contracts.",
        transport=("http",),
        endpoints=(),
        operations=("read", "write"),
        governance_supported=True,
        metadata={"aide_exposure": "not_exposed"},
    ),
    GatewayCapabilityContract(
        capability_id="digital_twin.dxs",
        name="DXS / Digital Twin Structure",
        owner="digitaltwin, tools.digital_twin, packages.simulation",
        status="contract_gap",
        description="Implementation exists, but no stable Gateway DXS contract was verified for client discovery.",
        transport=("internal",),
        endpoints=(),
        operations=("read", "execute"),
        evidence_supported=True,
        verification_supported=True,
        dependencies=("packages.simulation",),
        metadata={
            "implementation_locations": ["digitaltwin/", "tools/digital_twin/", "packages/simulation/"],
            "minimum_future_contract": (
                "Gateway read-only twin state and simulation result contract with evidence references."
            ),
        },
    ),
    GatewayCapabilityContract(
        capability_id="self_healing.loop",
        name="Self-Healing Loop",
        owner="packages.solution_architecture, packages.simulation, tools/scripts",
        status="contract_gap",
        description="Implementation exists but Gateway contract is not yet stable for client discovery/execution.",
        transport=("internal",),
        endpoints=(),
        operations=("execute",),
        evidence_supported=True,
        verification_supported=True,
        dependencies=("runtime.sandbox",),
        metadata={
            "implementation_locations": [
                "packages/solution_architecture/",
                "packages/simulation/application/self_healing_engine.py",
                "tools/",
                "scripts/",
            ],
            "minimum_future_contract": "Governed Gateway self-healing proposal/status/evidence contract.",
        },
    ),
    GatewayCapabilityContract(
        capability_id="spatial.future_interface",
        name="Future Spatial / 3D Interface",
        owner="future EAOS interface clients",
        status="contract_gap",
        description="No stable spatial/3D Gateway capability contract is present in this repository phase.",
        transport=("internal",),
        endpoints=(),
        operations=("read",),
        metadata={"aide_exposure": "not_exposed"},
    ),
)


def list_capability_contracts() -> list[GatewayCapabilityContract]:
    """Return explicit Gateway capability contracts and documented gaps."""

    return list(CAPABILITY_CONTRACTS)
