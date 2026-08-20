# Gateway Capability Registry Audit

Phase 8 adds an explicit, Gateway-owned capability contract registry. The
registry is discovery metadata only: it does not execute tasks, evaluate
policies, create evidence, mutate DXS, or infer capabilities by scanning files.

## Capability states

- `available`: implementation, owner, contract, runtime entry point, and a
  verifiable Gateway contract exist.
- `degraded`: implementation and contract exist, but runtime evidence proves a
  partial outage or limitation.
- `unavailable`: a registered external dependency or contract cannot currently
  be observed.
- `contract_gap`: implementation or domain code exists, but no stable Gateway
  contract is available for clients.

## Authoritative inventory

| Capability | Authoritative owner | Existing implementation | Existing API/contract | Transport | Read | Execute | Mutate | Runtime dependency | Evidence | Governance | Verification | Current status | AIDE exposure | Gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Health | `apps.api.routers.health` | Gateway health router | `GET /health` | HTTP | yes | no | no | API Gateway process | no | no | no | available | footer/health observation | none |
| Capability discovery | `apps.api.routers.capability_runtime` | Explicit `apps.api.app.capability_contracts` registry | `GET /v1/capabilities` | HTTP | yes | no | no | Gateway app | no | no | no | available | capability registry panel | none |
| Task lifecycle | `apps.api.task_lifecycle` | `TaskLifecycleService` | `POST /api/v1/control/execute`, `GET /api/v1/tasks/{task_id}`, `WS /api/v1/tasks/{task_id}/events` | HTTP + WebSocket | yes | yes | no | Gateway task lifecycle service | yes | yes | yes | available | task UX, inspector, footer | none |
| Execution/runtime | `apps.api.routers.resilience`, `engine.sandbox`, `packages.self_rewrite` | WASM sandbox and self-rewrite runtime | `POST /sandbox/wasm/execute`, `POST /self-rewrite/run` | HTTP | no | yes | yes | sandbox runtime | no | no | yes | available | not exposed as direct AIDE execution | AIDE intentionally avoids direct runtime execution |
| Governance | `apps.api.routers.governance`, `packages.evolution.infrastructure.rego_compiler`, `kernel.governance` | Governance router, policy evaluator, constitutional engines | `POST /governance/opa/evaluate`, `POST /governance/rego/compile-eval`, governance topology/constitution routes | HTTP | yes | yes | yes | Gateway governance packages | no | yes | no | available | displays Gateway task metadata | none for task metadata |
| Verification | `apps.api.task_lifecycle`, `kernel.governance.zkp_merkle`, telemetry fitness bridge | Task verification and ledger verifier | task status metadata, `POST /governance/ledger/verify-merkle`, telemetry fitness route | HTTP | yes | yes | no | Gateway runtime/kernel | yes | yes | yes | available | task panel/inspector metadata | broader verification catalog not exposed |
| Evidence | `apps.api.task_lifecycle`, `kernel.governance.zkp_merkle` | Task evidence refs and ledger verification | task status metadata, `POST /governance/ledger/verify-merkle` | HTTP | yes | yes | no | Gateway task lifecycle and ledger verifier | yes | yes | yes | available | evidence ref display only | no AIDE evidence store |
| DXS / digital twin | `digitaltwin`, `tools.digital_twin`, `packages.simulation` | Twin orchestrator, twin models, simulation use cases | no stable Gateway DXS endpoint verified | internal | internal only | internal only | no client mutation | digital twin/simulation modules | partial/internal | not proven at Gateway boundary | partial/internal | contract_gap | not exposed | needs read-only Gateway twin state and simulation result contract with evidence refs |
| Self-healing | `packages.solution_architecture`, `packages.simulation`, tools/scripts | self-healing adapter/engine/scripts | no stable Gateway self-healing contract verified | internal | no | internal only | potential mutation/repair | workspace commands, tests, simulation | partial/internal | not proven at Gateway boundary | partial/internal | contract_gap | not exposed | needs governed proposal/status/evidence/rollback contract |
| Memory | `apps.api.routers.memory_knowledge`, `packages.memory`, `packages.knowledge_graph` | memory repository and hybrid graph/vector adapter | `GET /v1/memory`, `POST /v1/memory/store`, `POST /memory/hybrid-search` | HTTP | yes | no | yes | Gateway memory repo/knowledge graph adapter | yes | no | no | available | not exposed in AIDE this phase | needs presentation-specific read/search UX contract decisions |
| Knowledge | `apps.api.routers.knowledge`, `packages.knowledge`, `packages.knowledge_graph` | knowledge repository/splay cache and graph adapters | Gateway knowledge routes and memory hybrid-search route | HTTP | yes | no | yes | knowledge repository/cache | no | no | no | available | not exposed in AIDE this phase | needs UX scope |
| Telemetry | `apps.api.routers.telemetry_performance`, `platforms.telemetry` | telemetry exporter/service and fitness bridge | `POST /telemetry/ingest`, `POST /telemetry/otlp/export-span`, `POST /telemetry/fitness-bridge/eval` | HTTP | no | yes | yes | telemetry platform services | no | no | yes | available | runtime observation only | no dedicated AIDE telemetry visualization yet |
| Security | `apps.api.routers.security`, security platforms/agents | security router and platform drivers | Gateway security router included in master router | HTTP | yes | yes | yes | security platform adapters | no | yes | yes | available | not exposed in AIDE this phase | needs client-safe discovery of security route details |
| Federation | `apps.api.routers.federation`, `packages.federation` | federation registry/use cases | Gateway federation router included in master router | HTTP | yes | yes | yes | federation registry | no | yes | no | available | not exposed in AIDE this phase | needs client-safe route details |
| Tenancy | `apps.api.routers.tenancy`, `packages.tenancy` | tenant registry and RLS adapter | Gateway tenancy router included in master router | HTTP | yes | yes | yes | tenant registry/RLS adapter | no | yes | no | available | not exposed in AIDE this phase | needs client-safe route details |
| Orchestration | `apps.api.routers.autonomous`, `agents`, `packages.autonomous` | autonomous loop use case and agent orchestrator | `POST /autonomous/run-cycle` | HTTP | no | yes | yes | autonomous repository/services | yes | yes | yes | available | not exposed in AIDE this phase | no direct human UX yet |
| Autonomous | `apps.api.routers.autonomous`, `packages.autonomous` | autonomous cycle use case | `POST /autonomous/run-cycle` | HTTP | no | yes | yes | autonomous repository/services | yes | yes | yes | available | not exposed in AIDE this phase | no direct human UX yet |
| Sandbox | `apps.api.routers.resilience`, `engine.sandbox` | WASM sandbox runtime | `POST /sandbox/wasm/execute` | HTTP | no | yes | no | WASM sandbox runtime | no | no | yes | available | not exposed as AIDE execution | AIDE must not use as local execution path |
| Spatial / 3D future | future EAOS clients | no stable module-level client contract verified | none | internal | no | no | no | none verified | no | no | no | contract_gap | not exposed | define future Gateway spatial capability contract first |

## Contract gaps intentionally left open

- **DXS/digital twin**: implementation exists, but no stable Gateway endpoint was
  verified. Minimum future contract: read-only twin state and simulation result
  endpoint with evidence references and governance/verification metadata.
- **Self-healing**: implementation exists, but no stable Gateway self-healing
  client contract was verified. Minimum future contract: governed proposal,
  lifecycle/status, evidence, verification, and rollback metadata.
- **Spatial/3D**: no stable Gateway contract was verified. Minimum future
  contract: explicit spatial capability metadata and read-only scene/twin access.

AIDE must not close these gaps by importing subsystem internals or inventing
presentation-local engines.
