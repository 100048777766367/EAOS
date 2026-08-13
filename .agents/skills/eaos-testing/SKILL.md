---
name: eaos-testing
description: EAOS testing and verification skill for pytest, regression tests, API/WebSocket tests, architecture tests, failure diagnosis, and rerun strategy.
---

# EAOS Testing and Verification — Behavioral Evidence Layer (v2)

## Mission

Act as the Behavioral Evidence Guardian for `D:\EAOS`.

Tests MUST prove intended behavior and contract compliance. A passing test command is valid evidence ONLY when tests exercise the real behavioral contract rather than superficial assertions.

---

## Testing Hierarchy

```text
Unit Tests (Pure domain & model logic)
  ↓
Integration / Component Tests (Ports, Adapters, Subsystems)
  ↓
Architecture Validation (Boundary & Dependency Invariants)
  ↓
Runtime & E2E Verification (Services, Endpoints, WebSockets)
  ↓
Regression Evidence (Pass/Fail delta against known contracts)
```

---

## Behavior Preservation Policy during REWRITE

When executing a `REWRITE` strategy:
1. **Identify Intended Behavior**: Extract domain contracts from specifications, interfaces, and caller expectations.
2. **Characterize Contract Tests**: Write or update tests that assert the intended contract BEFORE modifying implementation.
3. **Verify Negative State**: Confirm contract tests fail on the broken/unsound implementation.
4. **Execute Reconstruction**: Rebuild implementation coherently.
5. **Verify Positive State**: Confirm contract tests pass on the reconstructed code.
6. **Run Full Regression Suite**: Ensure no downstream callers or sibling modules were broken.

DO NOT rewrite code and then delete or weaken tests to force a green result.

---

## Prohibited Test Suppression Practices

The agent MUST NEVER:
- Delete failing unit or integration tests;
- Skip tests (`@pytest.mark.skip`) without explicit root-cause justification;
- Weaken assertions (e.g. replacing exact equality with `is not None`);
- Swallow exceptions or wrap failing assertions in silent `try/except`;
- Increase timeouts to mask deadlocks or performance regressions.

---

## Execution & Evidence Ledger

Run tests via repository-native entry points:
```powershell
uv run task test
```
or:
```powershell
uv run pytest tests/
```
Include `fitness/` when acceptance testing is configured.

Record exact counts in the Evidence Ledger:
- Collected
- Passed
- Failed
- Skipped
- Errors
- Exit Code

`PASS` requires exit code 0 with 0 failures and 0 unhandled errors.
