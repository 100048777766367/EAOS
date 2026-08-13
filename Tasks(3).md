# EAOS — MASTER TASK ROADMAP v2.0

## Authority

Tasks comply with `ARCHITECTURE_CONSTITUTION.md`, `EAOS_CONSTITUTION.md`, `GOVERNANCE.md`, and `SECURITY_POLICY.md`.

## Core Rule

`ERROR COUNT != WORK COUNT`

EAOS repairs root causes rather than blindly repairing individual errors.

Allowed strategies: `PATCH | REFACTOR | REWRITE | RECOVER | ESCALATE`

## Task Graph

```text
T01 Foundation
 ↓ T02 Control Plane
 ↓ T03 Repository Integrity & Recovery
 ↓ T04 Intent & Contracts
 ↓ T05 System Graph / Digital Twin
 ↓ T06 Memory Architecture
 ↓ T07 Change Strategy
 ↓ T08 Contract-First Reconstruction
 ↓ T09 Safe Autonomous Execution
 ↓ T10 Adaptive Verification
 ↓ T11 Failure Orchestration & Branching
 ↓ T12 Runtime / API / WebSocket
 ↓ T13 Security Enforcement
 ↓ T14 EAOS Integration Loop
 ↓ T15 Chat Domain Reconstruction
 ↓ T16 Agent Orchestration
 ↓ T17 Sandbox / Experiment / Digital Twin
 ↓ T18 Chat + Real Execution Convergence
 ↓ T19 Self-Critique / Convergence / Evolution
 ↓ T20 Enterprise Autonomous Engineering OS
```

---

# TASK 01 — FOUNDATION & GOVERNANCE BASELINE

**Goal:** Establish the immutable EAOS governance foundation.

**Work:** verify constitutional documents, L0–L7 authority, security boundaries, protected paths, architectural invariants, and contradictions between governing documents.

**Exit:** governance is coherent and enforceable.

**Failure:** `T01-F → governance-repair → reverify → T01/T02`

---

# TASK 02 — EAOS CONTROL PLANE

**Goal:** Build machine-readable state and orchestration infrastructure.

```text
.eaos/
├── constitution/ ├── governance/ ├── tasks/ ├── state/
├── contracts/ ├── schemas/ ├── policies/ ├── registry/
├── decisions/ ├── failures/ ├── recovery/ ├── evidence/
├── checkpoints/ ├── runtime/ ├── events/ ├── scenarios/ └── manifests/
```

Must represent `TASK → STATE → FAILURE → RECOVERY → EVIDENCE → CONVERGENCE`.

**Failure:** `T02-F → control-plane-reconstruct → reverify → T02/T03`

---

# TASK 03 — REPOSITORY INTEGRITY & RECOVERY

**Goal:** Prevent corrupted repositories from being mass-repaired blindly.

Detect mass modifications, syntax explosions, truncated files, malformed filenames, encoding corruption, unexpected generated changes, locked files, and suspicious working-tree state.

```text
Local defect        → PATCH
Bad structure       → REFACTOR
Broken logic        → REWRITE
Repository corrupt  → RECOVER
Uncertain/high risk → ESCALATE
```

**Hard gate:** `>20 widespread syntax errors OR mass unrelated corruption OR uncertain integrity → FREEZE MUTATION`.

**Failure:** `T03-F → recovery-branch → restore/reconstruct → verify → rejoin`

---

# TASK 04 — INTENT / CONTRACT / REQUIREMENT ENGINE

**Goal:** Convert user intent into an executable enterprise contract.

Every large task defines intent, acceptance criteria, functional/non-functional behavior, architecture, security, runtime constraints, dependencies, authority, and blast radius.

`PROMPT != IMPLEMENTATION SPECIFICATION`

**Failure:** `T04-F → intent-reconstruct → reverify → rejoin`

---

# TASK 05 — SYSTEM GRAPH / DIGITAL TWIN

**Goal:** Know what a change can affect before changing it.

Map modules, packages, ports, adapters, services, APIs, WebSockets, agents, databases, configuration, tests, and runtime processes.

Outputs: dependency graph, contract graph, runtime graph, impact graph, blast-radius estimate.

**Failure:** `T05-F → graph-rebuild → reverify`

---

# TASK 06 — MEMORY ARCHITECTURE

**Goal:** Preserve knowledge across tasks without confusing memory with authority.

Memory classes:
`CONSTITUTIONAL MEMORY | DECISION MEMORY | FAILURE MEMORY | TASK MEMORY | RUNTIME MEMORY`

Memory informs decisions but cannot override the Constitution. Failures remain retrievable after task completion.

**Failure:** `T06-F → memory-reconstruct → reverify`

---

# TASK 07 — AUTONOMOUS CHANGE STRATEGY

**Goal:** Decide how to change code before modifying it.

```text
SYMPTOM → ROOT CAUSE → INTENDED BEHAVIOR → AFFECTED BOUNDARY
→ BLAST RADIUS → PATCH/REFACTOR/REWRITE/RECOVER/ESCALATE → PROOF PLAN
```

Do not preserve broken implementation merely to minimize the diff.

**Failure:** `T07-F → strategy-review → reselect-strategy`

---

# TASK 08 — CONTRACT-FIRST RECONSTRUCTION

**Goal:** Define behavior before rewriting implementation.

Contracts cover domain, ports, adapters, API, WebSocket, persistence, runtime, and agents.

```text
CONTRACT TEST → IMPLEMENTATION → VERIFICATION
```

**Failure:** `T08-F → contract-repair → reverify`

---

# TASK 09 — SAFE AUTONOMOUS EXECUTION

**Goal:** Make `/antigravity` a bounded execution interface.

```text
OBSERVE → DIAGNOSE → PLAN → AUTHORITY CHECK → CHECKPOINT → MUTATE → VERIFY
```

Controls: command allowlist, filesystem boundaries, protected resources, checkpoint, rollback, diff inspection, blast-radius gate, evidence capture, mutation freeze.

**Failure:** `T09-F → rollback/recovery → reverify`

---

# TASK 10 — ADAPTIVE VERIFICATION

**Goal:** Verification matches risk and system state.

```text
compile → contract/unit tests → type check → lint/format
→ architecture → security → integration → runtime → E2E when required
```

Tools are verifiers, not architectural authorities. Ruff/Pytest/Mypy failures trigger diagnosis, not automatic mass rewriting.

**Failure:** `T10-F → T11`

---

# TASK 11 — FAILURE ORCHESTRATION & BRANCHING

**Goal:** Prevent one failed task from poisoning later tasks.

```text
TASK N
 ├─ PASS → TASK N+1
 └─ FAIL
     ↓ FAILURE-ID
     ↓ ROOT CAUSE
     ↓ AFFECTED BOUNDARY
     ↓ REPAIR BRANCH
        ├ PATCH
        ├ REFACTOR
        ├ REWRITE
        ├ RECOVER
        └ ESCALATE
     ↓ REVERIFY
     ├ PASS → REJOIN ORIGINAL GRAPH
     └ FAIL → NEW FAILURE BRANCH
```

Every failure records originating task, first symptom, root cause, affected files/modules, affected downstream tasks, checkpoint, strategy, responsible agent, repair evidence, verification evidence, and resolution status.

No downstream task may treat an unverified failed state as healthy.

Repeated failure: `same strategy fails → reassess → different strategy → reassess boundary → escalate/rewrite/recover`. No infinite retries.

**Failure:** `T11-F → failure-system-reconstruct`

---

# TASK 12 — RUNTIME / API / WEBSOCKET

**Goal:** Verify real runtime behavior, not merely UI appearance.

```text
Browser → Frontend → HTTP/WS URL → Port → Uvicorn → FastAPI
→ Router → Handler → Service → Port → Adapter → Provider
```

Verify startup, processes, ports, HTTP, WebSocket lifecycle, endpoint contracts, health, and runtime evidence.

**Failure:** `T12-F → runtime-repair → reverify`

---

# TASK 13 — SECURITY & GOVERNANCE ENFORCEMENT

**Goal:** Turn security policy into executable controls.

Protect `.git`, `.venv`, backups, secrets, credentials, databases, governance, evidence, checkpoints, and production resources.

Control commands, filesystem, MCP, network, destructive operations, secrets, approvals, and audit trail.

**Failure:** `T13-F → security-repair / ESCALATE`

---

# TASK 14 — EAOS INTEGRATED ENGINEERING LOOP

**Goal:** Connect all foundational systems.

```text
INTENT → GOVERNANCE → STATE → CONTRACT → GRAPH → STRATEGY
→ AUTHORITY → CHECKPOINT → EXECUTION → VERIFICATION → EVIDENCE
→ CONVERGENCE → MEMORY → NEXT TASK
```

EAOS must know what it is doing, why, authority, changes made, failures, failure origin, repair branch, verification state, and next safe action.

**Failure:** `T14-F → integration-repair → reverify`

---

# TASK 15 — CHAT DOMAIN RECONSTRUCTION

**Goal:** Rebuild Chat around real behavior, context, and execution.

Domains: session, message lifecycle, context assembly, memory, agent routing, tool routing, task creation, execution status, evidence, and recovery/error state.

```text
CHAT QUALITY = intent + context + memory + routing + execution + verification
```

Do not increase chat message volume to compensate for an incomplete execution pipeline.

**Failure:** `T15-F → chat-reconstruct → reverify`

---

# TASK 16 — AGENT ORCHESTRATION

**Goal:** Agents collaborate through explicit contracts.

Specialists: Architect, Repository Engineer, Verification, Testing, Runtime, Security, Recovery, Execution.

```text
ORCHESTRATOR → SPECIALIST → EVIDENCE → RETURN → NEXT SPECIALIST
```

Repeated failure triggers strategy change, not blind retry.

**Failure:** `T16-F → agent-reconstruct → reverify`

---

# TASK 17 — SANDBOX / EXPERIMENT / DIGITAL TWIN

**Goal:** Simulate high-risk changes before primary mutation.

```text
PREDICT → SIMULATE → MUTATE → VERIFY
```

Support what-if analysis, dependency impact, contract impact, blast radius, rollback rehearsal, and failure rehearsal.

**Failure:** `T17-F → sandbox-repair → reverify`

---

# TASK 18 — CHAT + REAL EXECUTION CONVERGENCE

**Goal:** Make Chat an actual execution interface.

```text
USER → CHAT → INTENT → TASK → AUTHORITY → AGENT → EXECUTION → EVIDENCE → CHAT
```

States: `PLANNED | AUTHORIZED | RUNNING | BLOCKED | FAILED | RECOVERING | VERIFYING | PASSED | ESCALATED`.

```text
CHAT       = interface
EXECUTION  = capability
STATE      = control-plane truth
```

**Failure:** `T18-F → chat-execution-repair → reverify`

---

# TASK 19 — SELF-CRITIQUE / CONVERGENCE / EVOLUTION

**Goal:** Determine whether a result is genuinely complete.

Check assumptions, untested paths, invariants, contracts, architecture, security, runtime, evidence completeness, regression risk, and convergence.

```text
implementation problem → implementation repair
architecture problem    → ADR proposal
governance problem      → human decision
constitutional problem  → human-only path
```

**Failure:** `T19-F → critique-repair / ADR`

---

# TASK 20 — ENTERPRISE AUTONOMOUS ENGINEERING OS

**Goal:** Integrate EAOS into a coherent autonomous engineering operating system.

```text
USER → CHAT → INTENT → GOVERNANCE → TASK → CAUSAL ANALYSIS
→ CHANGE STRATEGY → AGENT ORCHESTRATOR → SAFE EXECUTION
→ DIGITAL TWIN → VERIFICATION → EVIDENCE → CONVERGENCE
→ MEMORY → NEXT TASK
```

## Final Acceptance

EAOS is not PASS merely because a command exits 0.

```text
INTENT + CONTRACT + ARCHITECTURE + SECURITY + BEHAVIOR
+ RUNTIME + EVIDENCE + RECOVERY SAFETY + GOVERNANCE = CONVERGED
```

---

# UNIVERSAL FAILURE PROTOCOL

Applies to Tasks 1–20.

1. **FREEZE:** repository corruption, systemic breakage, or uncertain integrity → `FREEZE MUTATION`.
2. **RECORD:** create a unique Failure ID.
3. **DIAGNOSE:** identify symptom, first failing boundary, root cause, and downstream impact.
4. **BRANCH:** never contaminate the main task path with an unverified repair.
5. **REPAIR:** choose `PATCH | REFACTOR | REWRITE | RECOVER | ESCALATE`.
6. **VERIFY:** verify root cause and affected contracts, not only the original failing command.
7. **REJOIN:** only verified repair may rejoin the task graph.
8. **REPEATED FAILURE:** collect evidence → change strategy → reassess boundary → rewrite/recover/escalate if necessary.

---

# TASK STATE MACHINE

```text
PLANNED
 ↓
AUTHORIZED
 ↓
RUNNING
 ├──→ PASSED → REJOIN / NEXT
 └──→ FAILED → DIAGNOSING
                 ↓
          PATCH / REFACTOR / REWRITE / RECOVER
                 ↓
             VERIFYING
              ├──→ PASSED → REJOIN
              └──→ FAILED → NEW FAILURE BRANCH / ESCALATE
```

---

# SOURCE OF TRUTH

| Domain | Source |
|---|---|
| Constitution | Constitution files |
| Authority | Governance |
| Task definition | `Tasks.md` + task registry |
| Task state | State registry |
| Failure | Failure registry |
| Evidence | Evidence registry |
| Runtime | Runtime registry |
| Contracts | Contract registry |
| Architecture decisions | ADR registry |
| Recovery | Recovery/checkpoint registry |
| Event history | Append-only event ledger |
| Source | Git |

`Tasks.md` is the master roadmap, not the complete state database.

---

# COMPLETION HANDOFF CONTRACT

Every task must produce:

```text
status
strategy
files changed
contracts affected
tests
verification evidence
failures
recovery
unresolved risks
next eligible task
rejoin point
```

A task is **NOT complete** merely because files changed.

---

# EAOS GOLDEN RULES

1. `ERROR COUNT != WORK COUNT`.
2. Repair root causes, not symptoms.
3. Never continue blindly from a failed task.
4. Never use L4 authority to perform L6 architecture changes.
5. Never weaken tests to manufacture PASS.
6. Never weaken governance to make execution easier.
7. Never delete evidence.
8. Never overwrite checkpoints.
9. Never modify protected resources without authority.
10. Never retry the same failed strategy indefinitely.
11. Prefer coherent rewrite when implementation is demonstrably unsound.
12. Recover repository corruption before ordinary engineering.
13. Verify repaired boundaries before rejoining.
14. Preserve failure memory.
15. Treat Chat as an interface to real execution.
16. Treat every PASS as an evidence-backed claim.
17. Use ADRs for architectural evolution.
18. Require human authority for L6/L7.
