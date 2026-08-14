---
name: eaos-runtime-debugging
description: EAOS runtime troubleshooting skill for FastAPI, Uvicorn, ports, processes, startup/import failures, routing, dependencies, frontend/backend connectivity, and localhost diagnosis.
---

# EAOS Runtime Debugging — Operational Evidence Layer (v2)

## Mission

Act as the Operational Evidence Guardian for `D:\EAOS`.

Diagnose runtime failures through systematic layer inspection. Verify active listeners, process startup, protocol handshakes, and endpoint status using real runtime evidence.

---

## The Systemic Runtime Graph

When a runtime failure occurs, trace the exact layer of breakdown:

```text
Browser / Client UI
  ↓ (Port & Protocol Host Mapping)
TCP Listener (`netstat -ano`)
  ↓ (Uvicorn ASGI Server)
FastAPI Middleware Chain
  ↓ (Router & Route Matching)
Application Domain Handler
  ↓ (Port / Adapter Infrastructure: Neo4j, Postgres, Ollama)
HTTP Response / WebSocket Stream
```

---

## Systemic Root Cause vs Quick-Fix Workarounds

- **DO NOT** create workaround endpoints or duplicate server listeners to mask port/URL configuration mismatches.
- **DO NOT** swallow startup exceptions or wrap failing dependency calls in silent retries.
- **ALWAYS** trace the root cause back to its origin (configuration, missing route, uninitialized adapter, broken import) and fix the root cause.

---

## Port Assignment & Inspection

Standard EAOS Ports:
- `8000`: API Gateway / FastAPI
- `3002`: Web UI (Next.js / Vite)
- `7474`: Neo4j HTTP
- `9090`: Prometheus Metrics
- `11434`: Ollama LLM Service

To verify a port is actually listening:
```powershell
netstat -ano | findstr :8000
```
Do not infer server health merely from process startup text. Verify active socket listening and HTTP responses.

---

## Endpoint & Health Verification

Once process startup is confirmed, execute real HTTP checks:
```powershell
Invoke-WebRequest http://127.0.0.1:8000/health -UseBasicParsing
```
Verify status 200 and valid JSON response body.

---

## Operational Evidence Ledger

A runtime verification is `PASS` ONLY when:
1. The process starts without startup exceptions;
2. The expected port is actively listening;
3. Health endpoint (`/health`) returns HTTP 200;
4. Required WebSocket routes complete successful handshake and frame exchange;
5. All observations are recorded in the Evidence Ledger.
