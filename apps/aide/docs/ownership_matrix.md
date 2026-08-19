# AIDE Ownership / Boundary Matrix

AIDE is the Enterprise Engineering Gateway at the application,
presentation, and integration layer. Consume does not imply ownership.

| Path | Responsibility | Owner | AIDE dependency |
|------|----------------|-------|-----------------|
| `apps/aide/` | AIDE runtime application boundary | AIDE | Owns UI, presentation state, and client adapters. |
| `apps/aide/app/main.py` | FastAPI app entrypoint for AIDE only | AIDE | Runs `apps.aide.app.main:app` on port `6932`. |
| `apps/aide/app/adapters/` | Client-side adapters to external contracts | AIDE | Translates Gateway/platform state for AIDE UI. |
| `apps/aide/static/` | AIDE-owned browser assets | AIDE | Implements IDE surface modules. |
| `apps/aide/templates/` | AIDE-owned server-rendered templates | AIDE | Hosts only AIDE workspace HTML. |
| `apps/api/` | Enterprise/API Gateway | API | AIDE consumes REST/WebSocket contracts. |
| `apps/web/` | EAOS Web/control-room application | API/WEB | AIDE may deep-link; it does not absorb Web. |
| `frontend/src/features/editor/` | Editor R&D/reference when present | R&D / REFERENCE | Keep for research unless consumers prove retirement. |
| `designs/` | Shared design system/tokens/UX | DESIGN SYSTEM | AIDE consumes design direction without copying it. |
| `agents/` | Agent capability implementation | PLATFORM | AIDE presents and requests agent workflows. |
| `runtime/` | Runtime traces/process capability | PLATFORM | AIDE visualizes state through contracts. |
| `governance/` and `kernel/` | Governance and authority primitives | PLATFORM | AIDE displays governed outcomes only. |
| `memory/`, `knowledge/`, `packages/` | Shared knowledge/memory packages | SHARED | AIDE consumes through API/platform contracts. |
| `observability/` and telemetry platform | Metrics and traces | PLATFORM | AIDE visualizes observed state. |
| Databases, Redis, object stores, brokers | Deployment/infrastructure | INFRASTRUCTURE | AIDE never owns these services. |

## Anti-duplication decisions

- No `apps/aide/api/` directory is allowed for Gateway capability.
- No WebSocket server is implemented in AIDE while `apps/api` owns events.
- No Git or GitHub mutation backend is implemented in AIDE.
- UI labels use unknown/observed/degraded states until a backend probe or
  contract event supplies evidence.

## Phase 5 real Gateway integration audit

| Capability | Current Gateway contract | AIDE behavior |
| --- | --- | --- |
| Health | `GET /health` | Probe and render observed/degraded/unavailable. |
| Task submission | `POST /api/v1/control/execute` | Forward command requests; do not execute locally. |
| Task status | Missing in discovered API routers | Report missing capability gap. |
| Lifecycle/event streaming | Missing WebSocket route in this checkout | Report missing capability gap. |
| Runtime state | `GET /v1/capabilities` | Probe capability registry through Gateway. |
| Governance state | `POST /governance/opa/evaluate` | Consume Gateway policy evaluation contract. |
| Evidence/result | `POST /governance/ledger/verify-merkle` | Consume Gateway ledger verification contract. |

The current checkout cannot import `apps.api.app.main` because
`prometheus_fastapi_instrumentator` is not installed in the local environment.
AIDE therefore records Gateway HTTP failures as unavailable instead of showing
success.
