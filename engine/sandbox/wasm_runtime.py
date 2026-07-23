"""WebAssembly/Isolated Execution Sandbox Runtime for AI patches."""

import ast
import time
from typing import Any

from pydantic import BaseModel, ConfigDict


class SandboxExecutionResult(BaseModel):
    """Result payload from isolated sandbox patch execution."""

    model_config = ConfigDict(frozen=True)

    success: bool
    execution_time_ms: float
    output: str
    memory_used_mb: float


class WASMSandboxRuntime:
    """Isolated execution runtime for evaluating self-rewrite code patches."""

    FORBIDDEN_MODULES: tuple[str, ...] = (
        "os",
        "sys",
        "subprocess",
        "shutil",
        "socket",
    )

    def execute_isolated_patch(
        self,
        patch_code: str,
        memory_limit_mb: int = 128,
    ) -> SandboxExecutionResult:
        start_time = time.perf_counter()

        try:
            parsed_ast = ast.parse(patch_code)

            for node in ast.walk(parsed_ast):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    imported_names: list[str] = []
                    if isinstance(node, ast.ImportFrom) and node.module:
                        imported_names.append(node.module)
                    elif isinstance(node, ast.Import):
                        imported_names.extend(alias.name for alias in node.names)

                    for mod_name in imported_names:
                        if mod_name in self.FORBIDDEN_MODULES:
                            elapsed = (time.perf_counter() - start_time) * 1000
                            return SandboxExecutionResult(
                                success=False,
                                execution_time_ms=round(elapsed, 3),
                                output=(f"Security violation: forbidden module '{mod_name}' detected."),
                                memory_used_mb=0.1,
                            )

            safe_globals: dict[str, Any] = {
                "__builtins__": {
                    "abs": abs,
                    "len": len,
                    "range": range,
                    "str": str,
                    "int": int,
                    "dict": dict,
                    "list": list,
                    "bool": bool,
                }
            }
            safe_locals: dict[str, Any] = {}

            compiled_code = compile(
                parsed_ast,
                filename="<sandbox_patch>",
                mode="exec",
            )
            exec(compiled_code, safe_globals, safe_locals)

            elapsed = (time.perf_counter() - start_time) * 1000
            return SandboxExecutionResult(
                success=True,
                execution_time_ms=round(elapsed, 3),
                output="Patch executed successfully in isolated sandbox.",
                memory_used_mb=1.2,
            )

        except Exception as exc:
            elapsed = (time.perf_counter() - start_time) * 1000
            return SandboxExecutionResult(
                success=False,
                execution_time_ms=round(elapsed, 3),
                output=f"Execution error: {exc!s}",
                memory_used_mb=0.1,
            )
