# Rebuild Prompt Addendum Applied

The rebuild lifecycle now treats AIDE as an Enterprise Engineering Gateway at
the application and presentation layer. AIDE can present, integrate,
orchestrate UI, consume contracts, show observed state, and request governed
actions. It does not own shared backend implementations.

## Required locked decisions

- Target branch is expected to be `rebuild/aide-from-scratch` from
  `origin/main`; this checkout currently exposes only branch `work`.
- Legacy work remains a reference/preservation branch and is not a runtime
  implementation source for AIDE.
- Runtime entrypoint is `apps.aide.app.main:app` on `127.0.0.1:6932`.
- API remains `apps.api.app.main:app` on `127.0.0.1:8000`.
- Web remains `apps.web.app.main:app` on `127.0.0.1:3002`.
- AIDE-owned HTML stays under `apps/aide/templates/`.
- AIDE-owned scripts and styles stay under `apps/aide/static/`.
- Existing EAOS capabilities are consumed, not rewritten inside AIDE.

## Enterprise engineering domains surfaced by AIDE

01 Workspace / IDE; 02 AI / Copilot; 03 Agent Engineering; 04 Source Control;
05 Code Hosting / Collaboration; 06 Software Delivery; 07 Runtime /
Operations; 08 Governance / Control; 09 Evidence / Assurance; 10 Knowledge /
Memory; 11 Observability / Diagnostics; 12 Ecosystem / Platform;
13 Architecture; 14 Security; 15 Evolution / Change; 16 Enterprise Context.
