from __future__ import annotations

import shutil
import subprocess
import sys

from tools.doctor.dto import DiagnosticCheckDTO, SeverityLevel

"""Runtime Checker inspecting executables and minimum versions."""


class RuntimeChecker:
    """Checker validating Python >= 3.14 and CLI version requirements."""

    checker_id = "runtime"
    name = "Runtime Environment Checker"
    category = "Runtime"
    version = "2.0.0"
    priority = 10
    enabled = True

    def run(self) -> list[DiagnosticCheckDTO]:
        checks: list[DiagnosticCheckDTO] = []

        py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        is_valid_py = sys.version_info.major == 3 and sys.version_info.minor >= 14
        checks.append(
            DiagnosticCheckDTO(
                checker_id=self.checker_id,
                category=self.category,
                name="Python Version (>= 3.14)",
                severity=(SeverityLevel.PASS if is_valid_py else SeverityLevel.WARN),
                status="PASS" if is_valid_py else "WARN",
                message=f"Python {py_ver}",
            )
        )

        for tool in ["uv", "pytest", "ruff", "mypy", "git"]:
            path = shutil.which(tool)
            st = "PASS" if path else "FAIL"
            sev = SeverityLevel.PASS if path else SeverityLevel.ERROR
            ver_str = self._get_tool_version(tool) if path else "Missing"
            checks.append(
                DiagnosticCheckDTO(
                    checker_id=self.checker_id,
                    category=self.category,
                    name=f"Tool: {tool}",
                    severity=sev,
                    status=st,
                    message=(f"{ver_str} ({path})" if path else "Executable missing"),
                )
            )

        return checks

    def _get_tool_version(self, tool: str) -> str:
        try:
            res = subprocess.run(
                [tool, "--version"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            return (res.stdout or res.stderr).strip().splitlines()[0]
        except Exception:
            return "Installed"
