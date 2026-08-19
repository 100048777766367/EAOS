# EAOS AIDE

AIDE is the EAOS Enterprise Engineering IDE and Engineering Gateway UI.
It is an application boundary under `apps/aide/`, not a backend API clone.

## Run

```bash
uv run uvicorn apps.aide.app.main:app --host 127.0.0.1 --port 6932 --reload
```

## Ownership map

See `docs/ownership_matrix.md` for the path-level boundary matrix.


| Capability | Owner | AIDE responsibility |
| --- | --- | --- |
| IDE shell, activity bar, layout, tabs | AIDE | Implement client UI and state. |
| Monaco editor adapter | AIDE | Manage editor host, model lifecycle, diagnostics hooks. |
| Explorer, file search, inspector | AIDE | Render workspace UI and selected resource metadata. |
| Terminal UI | AIDE | Display governed terminal/session state. |
| Copilot and agent UI | AIDE | Collect prompts and show agent/task state. |
| Git and GitHub UI | AIDE | Surface status, diff, PR/check awareness safely. |
| REST and WebSocket backend | apps/api | Consumed through Gateway contracts only. |
| Governance, evidence, telemetry, runtime | EAOS platform/apps/api | Visualized by AIDE; not reimplemented here. |
| Design tokens | designs/ | Consumed as shared design direction; not copied. |
| Infrastructure services | infrastructure/platform | External services; not owned by AIDE. |

## Gateway contracts consumed

AIDE bootstraps HTTP and WebSocket contract metadata for health, agents,
chat streaming, runtime capabilities, governance, knowledge, and telemetry.
The implementation remains with `apps/api` and platform packages.

## Implemented client capabilities

- Workspace shell with header, explorer, editor, terminal, copilot, inspector,
  activity bar, runtime footer, responsive layout, and resizable-pane state.
- Gateway health is reported as observed/degraded/unavailable; AIDE does not
  hard-code backend success.
- JavaScript modules separated by responsibility under `static/js/`.
- Browser bootstrap state served by `/workspace/state`.
- Static assets and templates contained inside the AIDE boundary.
