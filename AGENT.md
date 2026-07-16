# EAOS Agent Bootstrap

This repository follows an Architecture-First engineering process.

Every AI agent MUST read and understand the project documentation before making any change.

---

# Required Reading Order

Read these documents completely in the following order:

1. docs/ARCHITECTURE_CONSTITUTION.md
2. docs/ENGINEERING_GUIDE.md
3. docs/PROJECT_CONTEXT.md
4. docs/CURRENT_CONTEXT.md
5. docs/TASK.md
6. docs/ADR_INDEX.md
7. docs/ROADMAP.md

These documents together define the authoritative state of the project.

Never skip them.

---

# Authority Order

If documents disagree, use this precedence.

1. ARCHITECTURE_CONSTITUTION.md
2. ENGINEERING_GUIDE.md
3. ADR_INDEX.md
4. PROJECT_CONTEXT.md
5. CURRENT_CONTEXT.md
6. ROADMAP.md
7. TASK.md

The Constitution always has highest priority.

---

# Before Any Change

Before editing any file:

* Read the required documents.
* Understand the current sprint.
* Understand active ADRs.
* Understand architectural constraints.
* Verify the requested work belongs to the current roadmap.

Do not guess.

If documentation is inconsistent, stop and explain the conflict.

---

# Architecture Rules

Architecture is considered approved.

Do not redesign the architecture.

Do not introduce new layers.

Do not invent new patterns.

Do not replace existing architecture without an ADR.

---

# Engineering Rules

Follow the Engineering Guide.

Respect repository structure.

Respect bounded contexts.

Respect dependency rules.

Respect naming conventions.

Respect coding standards.

Prefer existing capabilities over creating new ones.

---

# ADR Rules

Architecture changes require an ADR.

If implementation requires changing architecture:

STOP.

Explain why.

Wait for approval.

Never silently change architectural decisions.

---

# File Safety Rules

Never:

* delete existing files
* rewrite completed documents
* rename core directories
* move project structure

unless explicitly instructed.

Prefer incremental changes.

---

# Documentation Rules

After implementation, update documentation when necessary.

Possible updates include:

* CURRENT_CONTEXT.md
* TASK.md
* ADR_INDEX.md

Do not modify ARCHITECTURE_CONSTITUTION.md unless explicitly requested.

---

# Implementation Rules

Implement only what was requested.

Avoid unrelated refactoring.

Keep commits focused.

Minimize changes.

Preserve backward compatibility whenever possible.

---

# Completion Checklist

Before finishing:

* Documentation reviewed
* Architecture respected
* ADRs respected
* Current sprint respected
* Tasks updated if necessary
* No unauthorized architecture changes
* No unnecessary file modifications

---

# If Unsure

Never guess.

Stop.

Explain the uncertainty.

Request clarification.

Correctness is more important than speed.
