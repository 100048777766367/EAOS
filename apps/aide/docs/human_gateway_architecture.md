# AIDE Human Gateway Architecture

AIDE is a human interaction surface over EAOS contracts. It is not EAOS, and it
is not the authoritative runtime for any EAOS capability.

```text
Human
  ↓
Interface (AIDE or future UI)
  ↓
Client adapter / presentation route
  ↓
EAOS Gateway (`apps/api`)
  ↓
EAOS capability contract
  ↓
Authoritative subsystem
  ↓
Governance / verification / evidence / lifecycle
  ↓
Observable result presented back to the human
```

## Boundary statements

- AIDE is not EAOS.
- AIDE is not the execution engine.
- AIDE is not the governance engine.
- AIDE is not the evidence store.
- AIDE is not the verification engine.
- AIDE is not DXS.
- AIDE is not the memory engine.
- AIDE is not the self-healing engine.
- AIDE is a human interaction and visual access gateway over existing EAOS
  contracts.

## Ownership model

| Layer | Owner | AIDE responsibility |
| --- | --- | --- |
| Human interaction | AIDE and future clients | Collect commands, render state, preserve degraded/unavailable states |
| Thin client adapters | AIDE | Call existing Gateway contracts and transform responses for presentation |
| Gateway contracts | `apps/api` | Own HTTP/WebSocket boundaries for EAOS capabilities |
| Execution/lifecycle | Gateway/runtime subsystems | Own task IDs, lifecycle states, events, terminal close semantics, and errors |
| Governance | Gateway/governance packages | Own policy evaluation and governance decisions |
| Verification | Gateway/runtime subsystems | Own checks and verification results |
| Evidence | Gateway/kernel/subsystems | Own evidence IDs, references, ledger verification, and persistence |
| DXS/digital twin | `digitaltwin`, `tools/digital_twin`, simulation packages | Own twin state/simulation; AIDE must wait for Gateway contracts |

## Current essential bridge

AIDE currently exposes only the minimum stable path:

1. Observe Gateway health and capabilities.
2. Submit a human command through `POST /interactions/tasks`, which forwards to
   Gateway `POST /api/v1/control/execute`.
3. Treat `status=available` with Gateway payload `status=SUCCESS` as a successful dispatch even when the control route does not return a `task_id`; render any returned metadata without inventing IDs.
4. When the Gateway returns a real `task_id`, connect directly to Gateway `WS /api/v1/tasks/{task_id}/events` using the
   configured Gateway WebSocket base URL.
5. Apply each real event to one presentation pipeline that updates Task UX,
   Inspector, and Runtime Footer.
6. Preserve Gateway terminal states and evidence/error/correlation fields.

## Optionality requirement

EAOS must continue to operate when AIDE is stopped, removed, unavailable,
upgraded, or replaced. AIDE must continue to render available, degraded,
unavailable, or unsupported states when Gateway or a subsystem cannot be
observed. AIDE must never convert an unavailable contract into success.

## Future client compatibility

AIDE is one interface. CLI tools, API clients, mobile apps, voice interfaces,
3D/spatial/digital twin clients, simulation clients, robotics interfaces, and
automation surfaces must be able to converge on the same EAOS Gateway and
capability contracts without depending on AIDE.
