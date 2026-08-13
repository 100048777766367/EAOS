# EAOS DDD Bounded Contexts Package (`contexts/`)

## Business Capability
Domain-Driven Design (DDD) Bounded Contexts Registry, Context Map Relationships, and Domain Boundary Validation.

## Package Structure
- `crm/`: Customer Relationship Management Bounded Context (`crm_context.py`).
- `erp/`: Enterprise Resource Planning Bounded Context (`erp_context.py`).
- `finance/`: Financial Management & P&L Ledger Bounded Context (`finance_context.py`).
- `hr/`: Human Resources & Workforce Bounded Context (`hr_context.py`).
- `marketing/`: Marketing & Growth Funnels Bounded Context (`marketing_context.py`).
- `sales/`: Sales & Order Processing Bounded Context (`sales_context.py`).
- `context_registry.py`: Master Bounded Context Registry Engine & Context Map Generator.
