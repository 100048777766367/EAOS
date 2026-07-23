# EAOS Test Execution Runbook

> **Target Platform:** Pytest 9.x / Python 3.14  

---

## Standard Test Commands
- Run Full Test Suite: `uv run task test`
- Run Single Test File: `uv run pytest tests/unit/test_architecture_fitness.py`
- Run Coverage Report: `uv run pytest --cov=packages`