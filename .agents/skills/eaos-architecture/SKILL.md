---
name: eaos-architecture
description: EAOS architecture governance skill for Clean/Hexagonal Architecture, Ports and Adapters, dependency direction, package boundaries, Pydantic models, and ArchitectureValidator verification.
---

# EAOS Architecture Governance — Architecture Guardian (v2)

## Mission

Act as the Architecture Guardian for `D:\EAOS`.

Protect the Architecture Baseline (`FROZEN`) while governing controlled code evolution, enforcing Clean/Hexagonal Architecture boundaries, and preventing architectural drift.

---

## Authority Boundaries: Implementation vs Architecture

```text
IMPLEMENTATION REWRITE (L4)
   Allowed for AI if Root Cause Analysis indicates broken logic & contracts are preserved.

ARCHITECTURE BOUNDARY CHANGE (L6) / CONSTITUTION CHANGE (L7)
   PROHIBITED for autonomous AI execution.
   AI MUST propose an ADR (Architecture Decision Record) and STOP for Human Approval.
```

The agent assists architecture; humans govern architecture.

---

## Architectural Invariants (Hard Gates)

The agent MUST enforce these unalterable invariants:
1. **Clean Dependency Direction**: Inner layers (Domain/Kernel) MUST NEVER import outer layers (Infrastructure, Web frameworks, FastAPI, CLI handlers).
2. **Ports and Adapters Inversion**: Application logic MUST interact with infrastructure exclusively through declared Ports/Interfaces.
3. **No Logic in Handlers**: HTTP handlers, CLI entry points, and WebSocket endpoints MUST remain thin adapters; business logic belongs in domain services.
4. **No Direct Database Access**: Database operations MUST stay behind repository adapters.
5. **No Duplicate Abstractions**: Do not create parallel interfaces or duplicate models to circumvent existing validation.

---

## Pydantic v2 & Python 3.14 Conventions

- Use Pydantic v2 conventions (`ConfigDict`, explicit field validators).
- Maintain immutable domain value objects where part of the domain contract.
- Use Python 3.14 native type hints (`list[str]`, `dict[str, int]`, `str | None`). Avoid unnecessary `Any` or broad `# type: ignore`.

---

## Architecture Validation Workflow

Verify architectural compliance using the repository validator:
```text
ArchitectureValidator → validate_architecture() → ArchitectureValidationReport
```
Verify CLI exit code is 0 and no boundary errors are reported.

### Structural Verification Pipeline
1. Map affected modules and bounded contexts.
2. Identify target ports and interface contracts.
3. Update implementation/adapters.
4. Update behavior tests.
5. Run static analysis & type checks (`ruff`, `mypy`).
6. Run `validate_architecture()`.
7. Report boundary verification status in the Evidence Ledger.

