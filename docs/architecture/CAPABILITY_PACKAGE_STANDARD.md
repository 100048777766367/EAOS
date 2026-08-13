# EAOS Capability Package Architecture Standard v1.0

Every Business Capability in EAOS is managed as an isolated Capability Package.

## Package Directory Layout

capabilities/{capability_id}/
├── capability.md   # 16-Point Master Specification
├── workflow.md     # Business Process and AI Agent Flow
├── domain.md       # DDD Domain Models and Invariants
├── api.yaml        # OpenAPI 3.1 Contract
├── ui.md           # UI View Specification
├── tasks.md        # AI Coder Implementation Tasks
└── tests.md        # Acceptance Tests and Fitness Functions

## Implementation Mapping

- Domain: packages/{capability_id}/domain/models.py
- Application: packages/{capability_id}/application/use_cases.py
- API Router: apps/api/app/routers/{capability_id}.py
