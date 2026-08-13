---
name: eaos-repository-engineering
description: End-to-end repository engineering and verification workflow for EAOS. Use for dependency synchronization, repository checks, formatting, linting, type checking, tests, Task/Make validation, architecture validation, service startup, runtime checks, and final evidence reports.
---

# EAOS Repository Engineering — Reconstruction & Execution Engine (v2)

## Mission

Execute evidence-driven repository engineering, reconstruction, and pipeline verification for `D:\EAOS`.

The pipeline is evidence-driven. Do not infer success from configuration files or previous reports.

---

## Core Principle: Tools are Verifiers, Not Architectural Drivers

```text
TOOLS ARE VERIFIERS, NOT THE SOURCE OF ENGINEERING INTENT.
```

Static analysis tools (`ruff`, `mypy`, `pytest`, `compileall`) are diagnostic verifiers. They report symptoms. They DO NOT determine engineering intent or architectural design.

- **NEVER** run `ruff check --fix .` or `ruff format .` as a blind repair for structural/logic failures.
- **NEVER** suppress type errors or weaken assertions to achieve a green build.
- **ALWAYS** perform Root Cause Analysis to select the appropriate strategy (`PATCH`, `REFACTOR`, `REWRITE`, `RECOVER`) before invoking mutating tools.

---

## Safety & Protection Policy

Before any repository mutation:
1. Confirm working directory is `D:\EAOS`.
2. Inspect Git status (`git status --short`, `git diff --stat`).
3. Confirm protected paths are untouched:
   - `D:\EAOS\eaos_backups\`
   - `D:\EAOS\.venv\`
   - `D:\EAOS\.eaos_backups\`
   - `D:\EAOS\.eaos_contract_backup_*`
   - `D:\EAOS\.eaos-repair-backup\`
   - `D:\EAOS\.git\`
4. Never perform destructive cleanup (`git clean -fdx`, `docker volume prune`) as a verification prerequisite.

---

## Reconstruction & Pipeline Execution

### 1. Discovery & Boundary Isolation
Inspect existing source trees (`apps/`, `packages/`, `kernel/`, `engine/`, `tools/`, `services/`, `tests/`).
Determine authoritative source files vs generated artifacts. Do not edit generated output directly.

### 2. Dependency Synchronization
Run:
```powershell
uv lock
uv sync
```
If `uv.lock` changes, inspect the diff. Do not modify `.venv` directly.

### 3. Strategy-Driven Mutation
Apply changes according to the strategy determined by `eaos-verification`:
- **PATCH**: Apply minimal targeted fix.
- **REFACTOR**: Restructure code while preserving behavior and public contracts.
- **REWRITE**: Coherently reconstruct implementation from architecture, domain models, ports, and tests.
- **RECOVER**: Restore corrupted source files using Git history or verified backups.

### 4. Format Verification
Run:
```powershell
uv run ruff format .
```
Ensure Python lines remain under 88 characters per repository engineering policy.

### 5. Lint Verification
Run:
```powershell
uv run ruff check .
```
If lint errors occur, trace root cause rather than blindly applying auto-fixes across unrelated modules.

### 6. Type Check Verification
Run configured mypy checks:
```powershell
uv run mypy .
```
Preserve strict typing contracts. Do not use `# type: ignore` without explicit root-cause justification.

### 7. Behavior & Test Verification
Run configured test suite:
```powershell
uv run task test
```
or:
```powershell
uv run pytest tests/
```
Include `fitness/` when configured as part of acceptance scope. Record collected, passed, failed, skipped, and exit code.

### 8. Architecture Validation
Execute architecture validation:
```text
ArchitectureValidator → validate_architecture() → ArchitectureValidationReport
```
Verify CLI exit code is 0.

### 9. Runtime Boot & Health
Boot services and verify health endpoints:
```powershell
uv run uvicorn apps.api.app.main:app --host 127.0.0.1 --port 8000 --reload
```
Verify actual HTTP HEAD/GET status on `/health`, `/docs`, `/metrics`.

---

## Mass Diagnostic Protocol (e.g. 100+ or 254 errors)

When a verification command reports mass errors:
1. **FREEZE MUTATION**: Stop automatic fixing, formatting, or test-driven edits.
2. **INVESTIGATE INTEGRITY**: Run `git status` and `compileall` to check if repository integrity is compromised (`CORRUPTED`).
3. **ISOLATE BOUNDARY**: Determine whether errors originate from one broken abstraction or mass file corruption.
4. **SELECT STRATEGY**:
   - If corrupted → `RECOVER`.
   - If abstraction broken → `REWRITE` affected subsystem.
   - If localized → `PATCH`.
5. **VERIFY PIPELINE**: Execute complete pipeline from compile → test → lint → runtime.

---

## Evidence Ledger

Record every stage in the Evidence Ledger:
- Stage Name
- Exact Command Executed
- Exit Status / Status Code
- Evidence Snippet
- Result (`PASS` / `FAIL` / `UNVERIFIED`)

`PASS` requires executable evidence for all mandatory stages.

