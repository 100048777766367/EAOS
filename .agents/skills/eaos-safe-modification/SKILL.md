---
name: eaos-safe-modification
description: Safety and mutation-control skill for EAOS. Use before repository-wide edits, automated fixes, cleanup, generated changes, backup-sensitive work, or infrastructure mutations.
---

# EAOS Safe Modification — Change Control & Blast Radius Engine (v2)

## Mission

Act as the Change Control & Safety Guardian for `D:\EAOS`.

Enable autonomous engineering while strictly bounding mutation scope, enforcing Blast Radius policies, protecting system assets, and freezing writes upon repository integrity degradation.

---

## Protected Paths & Immutable Assets

The agent MUST NEVER delete, overwrite, format, rename, clean, or bulk-rewrite protected content:
```text
D:\EAOS\eaos_backups\
D:\EAOS\.venv\
D:\EAOS\.eaos_backups\
D:\EAOS\.eaos_contract_backup_*\
D:\EAOS\.eaos-repair-backup\
D:\EAOS\.git\
```

Discover additional backup or snapshot directories before broad automated operations. Backups are protected enterprise assets, NOT disposable build artifacts.

---

## Blast Radius Risk Matrix

Before applying any modification, evaluate the **Blast Radius**:

| Level | Scope | Criteria | Required Governance |
|---|---|---|---|
| `LOCAL` | 1–3 files | Single component fix | Standard execution |
| `SMALL` | 4–20 files | Multiple components | Pre-mutation git diff snapshot |
| `BROAD` | 20–100 files | Cross-subsystem scope | Root Cause Approval Gate + Full verification |
| `MASS` | 100+ files | Systemic change / Mass errors | **FREEZE MUTATION** + Repository Integrity Investigation |
| `SYSTEMIC` | Cross-boundary | Architecture / Security / Schema | **ESCALATE** (L6/L7) + ADR Proposal |

As Blast Radius increases, verification requirements and authority constraints MUST escalate automatically.

---

## Repository Corruption Guard & Mutation Freeze

If any of the following occur during verification:
- More than 20 syntax errors appear in a single run;
- Multiple unrelated packages report identical syntax corruption;
- Filenames appear malformed;
- Import statements or headers are systematically truncated;
- Indentation or encoding errors span unrelated modules;
- Git status reports unexpected mass modifications;

The agent MUST IMMEDIATELY:
1. **FREEZE MUTATION**: Stop all write operations immediately.
2. **STOP AUTO-FIX**: Disable `ruff --fix`, formatting, and test-driven mass edits.
3. **INSPECT GIT**: Run `git status --short` and `git diff --stat`.
4. **CLASSIFY INTEGRITY**: Declare system state as `DEGRADED` or `CORRUPTED`.
5. **ISOLATE CAUSE**: Determine whether corruption stems from working-tree mutation, bad script generation, encoding mismatch, or environment breakage.
6. **APPLY RECOVER STRATEGY**: Restore working tree to a known-good revision via Git before proceeding.

A mass diagnostic event is classified as a **REPOSITORY_INTEGRITY Incident**, NOT an ordinary repair task.

---

## Prohibited Destructive Operations

The agent MUST NOT run the following commands automatically:
```powershell
git clean -fd
git clean -fdx
docker compose down -v
docker system prune
docker volume prune
Remove-Item -Recurse -Force
```
Destructive operations require explicit human authorization.

---

## `.venv` and Dependency Protection

- **NEVER** edit files inside `D:\EAOS\.venv\`.
- Use `uv sync` or `uv lock` for dependency management. Direct virtual environment mutation is prohibited.

---

## Verification After Mutation

Every mutation MUST be followed by:
1. `git diff --stat` inspection;
2. Targeted syntax / compile verification (`python -m compileall`);
3. Behavior test run;
4. Broader pipeline verification if shared code changed.
