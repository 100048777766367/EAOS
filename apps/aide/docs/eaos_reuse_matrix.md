# EAOS Capability Reuse Matrix for AIDE

AIDE is a human interaction surface over EAOS contracts. This audit records
where an EAOS capability already exists, whether it is reachable through a
stable contract, and whether AIDE should consume, adapt, or leave it alone.

## Status legend

- **A. DIRECTLY CONSUMABLE** — AIDE can consume the contract now.
- **B. CONSUMABLE THROUGH EXISTING GATEWAY** — Capability is already exposed by
  `apps/api`; AIDE should call the Gateway instead of the subsystem directly.
- **C. NEEDS THIN ADAPTER** — The backend capability exists, but AIDE requires a
  small presentation/client adapter to call or display the existing contract.
- **D. CONTRACT GAP** — Capability exists or is implied, but no stable Gateway
  contract is available for AIDE in this phase.
- **E. NOT READY / DO NOT TOUCH** — Capability is research, internal, or unsafe
  to expose through AIDE without a future contract.

## Reuse matrix

| Capability | Existing owner | Existing contract | Existing runtime | AIDE consumer needed | Reuse method | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Capability discovery | `apps/api` + `packages/capability` | `GET /v1/capabilities` | `InMemoryCapabilityRegistry` in `apps.api.app.container` | Yes: show available/degraded/unavailable capability state | AIDE calls Gateway snapshot/contracts adapters | A. DIRECTLY CONSUMABLE |
| Gateway health | `apps/api` | `GET /health` | API Gateway process on `:8000` | Yes: footer/workspace health observation | AIDE health probe only; no local health synthesis | A. DIRECTLY CONSUMABLE |
| Task submission | `apps/api` | `POST /api/v1/control/execute` | `TaskLifecycleService.submit` | Yes: human command submission | Existing AIDE `/interactions/tasks` forwards to Gateway and accepts dispatch success without fabricating task IDs | B. CONSUMABLE THROUGH EXISTING GATEWAY |
| Task status | `apps/api` | `GET /api/v1/tasks/{task_id}` | `TaskLifecycleService.get` | Yes: task panel/inspector status read | Existing AIDE `/interactions/tasks/{task_id}` reads Gateway | B. CONSUMABLE THROUGH EXISTING GATEWAY |
| Task lifecycle events | `apps/api` | `WS /api/v1/tasks/{task_id}/events` | `TaskLifecycleService.events_for` + Gateway WebSocket | Yes: browser lifecycle stream | Browser connects to Gateway WS URL from bootstrap config | A. DIRECTLY CONSUMABLE |
| Governance result for task lifecycle | `apps/api` + `packages/evolution.infrastructure.rego_compiler` | Included in task response metadata/status DTO; standalone `POST /governance/opa/evaluate` and `/governance/rego/compile-eval` exist | Gateway policy evaluator container singleton | Yes: display only | Present Gateway-provided governance metadata; do not evaluate in AIDE | B. CONSUMABLE THROUGH EXISTING GATEWAY |
| Verification result for task lifecycle | `apps/api` | Included in task response metadata/status DTO | Gateway-owned task verification transition | Yes: display only | Present Gateway-provided verification metadata | B. CONSUMABLE THROUGH EXISTING GATEWAY |
| Evidence reference/result | `apps/api` + `kernel.governance.zkp_merkle` | Task evidence metadata/status DTO; standalone `POST /governance/ledger/verify-merkle` | Gateway task evidence object and ledger verifier | Yes: display only | Present evidence IDs/refs returned by Gateway; no AIDE evidence store | B. CONSUMABLE THROUGH EXISTING GATEWAY |
| Runtime/system observation | `apps/api`, `platforms.telemetry`, `platforms.performance`, capability registry | `GET /v1/capabilities`; telemetry/performance endpoints exist | Gateway routers and platform singleton services | Yes: footer/snapshot only | Observe Gateway health/capability state; avoid runtime control UI until contracts stabilize | C. NEEDS THIN ADAPTER |
| Memory / knowledge | `apps/api` + `packages/memory` + `packages/knowledge_graph` | `GET /v1/memory`, `POST /v1/memory/store`, `POST /memory/hybrid-search` | `memory_repo`, `knowledge_graph_adapter` | Not in essential path beyond registry rendering | Future AIDE presentation may call Gateway read/search contracts; no local memory engine | B. CONSUMABLE THROUGH EXISTING GATEWAY |
| DXS / Digital Twin Structure | `digitaltwin`, `tools/digital_twin`, `packages/simulation` | No stable Gateway DXS route found in current API router inventory | `EnterpriseDigitalTwinOrchestrator`, simulation use cases/adapters | No direct UI in this phase | Document only; future Gateway adapter required before AIDE UI | D. CONTRACT GAP |
| Runtime execution / sandbox | `apps/api` + `engine.sandbox` + `packages/self_rewrite` | `POST /sandbox/wasm/execute`, `POST /self-rewrite/run`, `POST /autonomous/run-cycle` | Gateway routers instantiate/use existing sandbox/self-rewrite/autonomous services | Not exposed as direct AIDE execution | Do not create AIDE execution path; task lifecycle remains entry path | E. NOT READY / DO NOT TOUCH |
| Orchestration / autonomous loop | `apps/api`, `agents`, `packages/autonomous`, `agents/orchestrator.py` | `POST /autonomous/run-cycle`; agent app entrypoint exists | Autonomous use cases and agent swarm | Not essential for this phase | Leave behind Gateway contracts; do not duplicate orchestration in AIDE | E. NOT READY / DO NOT TOUCH |
| Self-healing | `packages/solution_architecture`, `packages/simulation`, scripts/tools | No stable AIDE-facing Gateway contract found | Self-healing adapter/scripts and simulation healing modules | No | Document gap; do not expose/duplicate | D. CONTRACT GAP |
| Telemetry / observability | `apps/api` + `platforms.telemetry` | `POST /telemetry/ingest`, `POST /telemetry/otlp/export-span`, `POST /telemetry/fitness-bridge/eval` | Telemetry exporter/service | Registry rendering only in this phase | Future visual adapter only; no AIDE telemetry engine | B. CONSUMABLE THROUGH EXISTING GATEWAY |
| Federation / tenancy / security | `apps/api` + respective packages/platforms | Existing Gateway routers included in `master_router` | Existing Gateway/application services | No direct AIDE feature in this phase | Discover later through Gateway capability contracts | D. CONTRACT GAP for AIDE UI |
| Explorer/editor/git/terminal presentation | `apps/aide` | AIDE static/browser modules only | Browser state only | Already present | UI-only; no filesystem/Git/terminal backend mutation | A. DIRECTLY CONSUMABLE as presentation only |

## Essential path selected for this phase

1. Capability discovery via `GET /v1/capabilities`.
2. Gateway health via `GET /health`.
3. Task submission via `POST /api/v1/control/execute` through AIDE's existing
   interaction route.
4. Task status via `GET /api/v1/tasks/{task_id}` through AIDE's existing read
   route.
5. Task lifecycle events via `WS /api/v1/tasks/{task_id}/events`.
6. Governance, verification, evidence, correlation, and error metadata as
   Gateway-owned fields on task responses/events.
7. AIDE presentation in Task UX, Inspector, and Runtime Footer.

## Explicit non-goals

AIDE does not implement DXS, execution, orchestration, governance, evidence,
verification, self-healing, memory, persistence, Git mutation, terminal
execution, scheduling, queues, cancellation, timeout, or lease ownership.
