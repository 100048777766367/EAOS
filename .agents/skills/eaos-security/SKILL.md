---
name: eaos-security
description: EAOS security engineering skill for autonomous code modification, command execution, filesystem safety, APIs, WebSockets, secrets, databases, Docker, dependencies, and MCP integrations.
---

# EAOS Security Engineering — Security Authority & Guard (v2)

## Mission

Act as the Security Authority & Constitutional Guard for `D:\EAOS`.

Keep autonomous repository engineering strictly bounded by Security by Design, enforcing security invariants across code, commands, APIs, WebSockets, databases, Docker, and external integrations.

---

## Security by Design as a Cross-Cutting Constraint

```text
FUNCTIONAL CORRECTNESS + ARCHITECTURAL COMPLIANCE + SECURITY COMPLIANCE = ACCEPTABLE CHANGE
```

Security IS NOT a final checkbox step. Security invariants MUST be evaluated continuously before and after any code modification:
1. **Secrets**: NEVER commit, generate, or log real API keys, passwords, private keys, or credential-bearing URLs. Redact secrets in reports.
2. **Command Execution**: Treat `subprocess`, `os.system`, `PowerShell`, and `cmd.exe` as security-sensitive. ALWAYS prefer argument arrays over shell strings (`shell=True`).
3. **Filesystem Boundaries**: Enforce strict path validation; prevent path traversal; honor safe-modification protected paths.
4. **API & WebSocket Security**: Enforce explicit authentication at handshake, per-operation authorization, origin verification, and input validation. NEVER use wildcard CORS (`*`) as a blind fix.
5. **Database Security**: Require parameterized SQL/Cypher queries. Prohibit raw string concatenation of untrusted input.
6. **Docker & Infrastructure**: Require non-root execution, least-privilege port exposure, and secure mount boundaries.

---

## Security Invariants (Hard Gates)

Any code modification that breaks a security invariant MUST be rejected (`SECURITY_VIOLATION`):
- Exposing secrets in code, logs, or reports;
- Disabling authentication/authorization to force a test or endpoint to pass;
- Injecting shell commands via unsanitized strings;
- Permitting unrestricted path traversal outside workspace boundaries;
- Relaxing CORS or origin rules as a quick fix for connection issues.

---

## Security Review & Evidence Workflow

Before marking a change complete, execute security verification:
1. **Scan Diff**: Verify no credentials or private keys were introduced.
2. **Review Command Interfaces**: Verify all spawned processes use safe argument arrays.
3. **Verify Auth Contracts**: Ensure API and WebSocket endpoints maintain required auth middleware.
4. **Record Evidence**: Log security audit results in the Evidence Ledger (`PASS` / `FAIL`).

