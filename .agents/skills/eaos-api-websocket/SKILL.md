---
name: eaos-api-websocket
description: EAOS HTTP and WebSocket verification skill for chat endpoints, API/UI port mismatches, routing, CORS, proxying, connection lifecycle, and frontend-backend integration.
---

# EAOS API & WebSocket — Specialized Contract Verifier (v2)

## Mission

Act as the Specialized Contract Verifier for `D:\EAOS`.

Verify exact HTTP and WebSocket contracts, route registrations, CORS policies, port mappings, frame serialization, and connection lifecycles between EAOS frontend clients and backend services.

---

## Protocol Discovery & Contract Mapping

Before testing any endpoint (e.g., `/chat`), inspect source code to map the exact contract:
- HTTP GET / POST (Request / Response JSON schema)
- WebSocket (`ws://` or `wss://` frame exchange protocol)
- Server-Sent Events (SSE) / Chunked Streaming
- Reverse Proxy Route (`/api/...`)

Never guess the protocol or test arbitrary routes without checking route registration in code.

---

## Single Source of Truth for Configuration

Frontend configuration variables (`API_BASE_URL`, `VITE_API_URL`, `NEXT_PUBLIC_WS_URL`) MUST align with backend server listeners.

- **DO NOT** add duplicate endpoint listeners or workaround proxies to mask a client configuration error.
- **DO NOT** use wildcard CORS (`*`) as a blind production fix. Fix origin configuration at the source.

---

## WebSocket Verification Lifecycle

A WebSocket contract is `PASS` ONLY when all stages succeed with evidence:
```text
1. Server process listening on designated port
2. WebSocket route registered in FastAPI
3. Handshake HTTP 101 Switch Protocols succeeds
4. Outbound frame sent successfully
5. Inbound response frame received matching contract schema
6. Connection close / error lifecycle handled cleanly
```

---

## Contract Failure Classification

Classify contract failures as:
- Route absent in router registration;
- HTTP method mismatch (e.g. GET instead of POST);
- Host / Port mismatch between client config and server bind;
- Protocol mismatch (HTTP vs WS);
- CORS / Origin policy rejection;
- Serialization / Pydantic schema validation error;
- WebSocket handshake timeout.

Record exact failure classification and root cause in the Evidence Ledger.

