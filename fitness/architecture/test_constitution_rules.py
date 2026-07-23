"""Fitness Functions verifying EAOS Architecture Constitution Rules."""

import ast
from pathlib import Path


def test_rule_r04_domain_isolation_no_infrastructure_imports() -> None:
    """R4: Stable Core — Domain layer must not import infrastructure."""
    domain_dir = Path("packages/governance/domain")
    if not domain_dir.exists():
        return

    forbidden = {"sqlalchemy", "fastapi", "httpx", "psycopg2", "openai"}
    for py_file in domain_dir.rglob("*.py"):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] not in forbidden
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert node.module.split(".")[0] not in forbidden


def test_rule_r12_r14_domain_isolation_no_llm_sdk() -> None:
    """R12/R14: Model Agnostic — Domain must not import LLM SDKs."""
    domain_dir = Path("packages")
    if not domain_dir.exists():
        return

    llm_sdks = {"openai", "anthropic", "langchain", "litellm"}
    for py_file in domain_dir.rglob("domain/**/*.py"):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] not in llm_sdks
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert node.module.split(".")[0] not in llm_sdks
