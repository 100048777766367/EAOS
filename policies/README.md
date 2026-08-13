# EAOS Declarative Policy Manifests & Policy as Code Package (`policies/`)

## Business Capability
Policy as Code (OPA Rego), ISO 27001 Compliance Manifests, Clean Code Engineering Policies, AI Governance Policies, Zero Trust Security, and Assembly Voting Governance.

## Package Structure
- `ai/`: AI Governance Policies (`ai_policy.py`, `ai_governance_policy.yaml`).
- `architecture/`: Retention & Boundary Policies (`architecture_policy.py`).
- `compliance/`: ISO 27001 Compliance (`compliance_policy.py`).
- `engineering/`: Clean Code & PEP 8 Policies (`engineering_policy.py`).
- `governance/`: Assembly Voting & BFT Policies (`governance_policy.py`).
- `quality/`: Zero-Ops Quality Gates Policies (`quality_policy.py`).
- `security/`: Zero Trust Rego & Hyperscale Security (`policy.py`, `rbac.rego`, `zero_trust.rego`).
- `policy_manifest_loader.py`: Master Policy Manifests & OPA Loader.
