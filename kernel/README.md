# EAOS Frozen Core Kernel (`kernel/`)

> **Status:** FROZEN (CENTENNIAL EDITION)
> **Authority:** Supreme Source of Kernel Truth

## Business Capability
Frozen Core Kernel providing zero-dependency primitives, Merkle governance ledgers, event bus streaming, Raft & Synod BFT federation, and closed cybernetic runtime loops.

## Sub-Modules Architecture
1. **`common/`** — Circuit breaker & resilience mechanisms (`resilience.py`).
2. **`contracts/`** — Kernel protocol contracts (`kernel_contracts.py`).
3. **`events/`** — Event Bus, Schema Registry, and Stream Replay.
4. **`federation/`** — Raft Consensus, Synod BFT, and CRDT Cross-Region Sync.
5. **`governance/`** — Constitution Amendment Engine, Merkle Ledger, and Cybernetic Loop Engine.
6. **`policies/`** — Frozen Kernel Constitutional Invariants (`kernel_policies.py`).
7. **`primitives/`** — Immutable Core Value Objects (`kernel_primitives.py`).
8. **`registry/`** — Enterprise Registry Engine.
9. **`runtime/`** — Continuous Improvement Runtime Engine & Main Entrypoint.
10. **`kernel_orchestrator.py`** — Master Kernel Integrity Auditor.
