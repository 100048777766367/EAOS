# EAOS AI Agent Operational Directive

> **Target Audience:** Autonomous AI Coding Agents (Claude Code, Cursor, Aider)  
> **Governance:** ARCHITECTURE_CONSTITUTION.md v2.0  

---

## Mandatory Execution Rules
1. **Line Length:** Every line MUST be strictly under 88 characters.
2. **Domain Isolation:** Zero framework code (FastAPI/SQLAlchemy) inside domain.
3. **Type Annotations:** 100% explicit PEP 585/604 annotations (dict[str, Any]).
4. **Quality Verification:** Run uv run task lint, uv run task test, and 
   uv run task validate after generating code.