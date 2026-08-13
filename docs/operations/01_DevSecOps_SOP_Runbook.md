# 01. EAOS DevSecOps Incident Response & Quality Gates SOP

## 1. Incident Classification Matrix

| Level | Impact | Response SLA | Target Resolution |
| :--- | :--- | :--- | :--- |
| **P1 - Critical Outage** | Full API Gateway or Database Down | **< 5 minutes** | < 1 hour |
| **P2 - Major Degradation** | Service degradation or Single DB offline | **< 15 minutes** | < 4 hours |
| **P3 - Minor Issue** | Linter/Type warning or minor drift | **< 4 hours** | < 24 hours |
| **P4 - Advisory** | Optimization / Refactoring request | **< 24 hours** | Next Sprint |

---

## 2. P1 Critical Incident Handling SOP

1. **Detect & Alert:**
   - Execute CLI Doctor: `uv run python -m tools.cli.main doctor`
   - Observe failing checks in `Infrastructure` or `Architecture Validator`.
2. **Immediate Containment:**
   - Isolate failing service container: `docker restart eaos-postgres-prod`
   - Check fallback mode status in Control Room (`:8000/chat`).
3. **Diagnose & Trace:**
   - Inspect trace logs in `runtime/logs/` or run `uv run python -m tools.cli.main runtime`.
4. **Apply Patch or Undo:**
   - If caused by bad code: Click **`↩️ Hoàn Tác`** in `:8000/chat` or execute `POST /api/v1/control-room/undo`.
   - If caused by config: Re-apply `.env` configuration.
5. **Post-Mortem & Evidence:**
   - Run Quality Gates: `uv run task lint`, `uv run task test`, `uv run task validate`.
