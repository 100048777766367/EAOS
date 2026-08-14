# EAOS Agent Task / Execution Subsystem

This package owns task lifecycle and execution boundaries.

## Current responsibility

```text
AgentOrchestrator
    |
    v
TaskManager
    |
    +--> TaskPlanner
    |
    +--> TaskExecutor
```

The subsystem intentionally does not mutate the repository.

## Lifecycle

```text
CREATED
  -> PLANNED
  -> ASSIGNED
  -> EXECUTING
  -> VERIFYING
  -> COMPLETED / FAILED
```

Verification is an external boundary. The existing chat verification subsystem
owns Ruff, Pytest, aggregation, and evidence.

Future repository mutation must pass through MutationPort and the EAOS
governance/safety layer.
