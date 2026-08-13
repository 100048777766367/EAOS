"""Registry managing CLI commands (Open/Closed Principle)."""

from __future__ import annotations

from typing import cast

from tools.cli.base import BaseCLICommand
from tools.cli.dto import CLIContextDTO, CLIExitCode
from tools.cli.services import (
    BenchmarkCLIService,
    DoctorCLIService,
    RuntimeCLIService,
    ValidateCLIService,
)


class DoctorCommand:
    """CLI Command for system diagnosis."""

    command_name = "doctor"
    help_text = "Diagnose enterprise system health"

    def __init__(self) -> None:
        self.service = DoctorCLIService()

    def execute(self, ctx: CLIContextDTO) -> CLIExitCode:
        return self.service.run_doctor(ctx)


class ValidateCommand:
    """CLI Command for architecture validation."""

    command_name = "validate"
    help_text = "Validate architecture boundary rules"

    def __init__(self) -> None:
        self.service = ValidateCLIService()

    def execute(self, ctx: CLIContextDTO) -> CLIExitCode:
        return self.service.run_validation(ctx)


class RuntimeCommand:
    """CLI Command for managing 24/7 background production daemon."""

    command_name = "runtime"
    help_text = "Manage 24/7 background production daemon and stack"

    def __init__(self) -> None:
        self.service = RuntimeCLIService()

    def execute(self, ctx: CLIContextDTO) -> CLIExitCode:
        return self.service.run_status(ctx)


class BenchmarkCommand:
    """CLI Command for running Chaos & Benchmark suite."""

    command_name = "benchmark"
    help_text = "Run Chaos Engineering & Benchmark suite on Swarm/RAG"

    def __init__(self) -> None:
        self.service = BenchmarkCLIService()

    def execute(self, ctx: CLIContextDTO) -> CLIExitCode:
        return self.service.run_benchmark_suite(ctx)


class ControlPlaneCommand:
    """CLI Command for EAOS Control Plane Execution & Audit."""

    command_name = "control-plane"
    help_text = "Execute EAOS Control Plane state machine, audit & strategy evaluation"

    def execute(self, ctx: CLIContextDTO) -> CLIExitCode:
        from kernel.control_plane.cli import EAOSControlPlaneCLI

        cli = EAOSControlPlaneCLI(workspace_root=ctx.workspace_root)
        res = cli.run_control_plane_audit()
        print("==========================================")
        print("     EAOS CONTROL PLANE AUDIT REPORT      ")
        print("==========================================")
        for k, v in res.items():
            print(f"  {k:<20}: {v}")
        print("==========================================")
        val = 0 if res["status"] == "PASS" else 1
        return cast(CLIExitCode, val)


class CLICommandRegistry:
    """Registry providing extensible CLI commands."""

    def __init__(self) -> None:
        self._commands: dict[str, BaseCLICommand] = {}
        self._register_default_commands()

    def _register_default_commands(self) -> None:
        self.register(DoctorCommand())
        self.register(ValidateCommand())
        self.register(RuntimeCommand())
        self.register(BenchmarkCommand())
        self.register(ControlPlaneCommand())

    def register(self, command: BaseCLICommand) -> None:
        """Register a new CLI command dynamically."""
        self._commands[command.command_name] = command

    def get_command(self, name: str) -> BaseCLICommand | None:
        """Retrieve command by name."""
        return self._commands.get(name)

    def list_commands(self) -> list[BaseCLICommand]:
        """Return list of registered commands."""
        return list(self._commands.values())
