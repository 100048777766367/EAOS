from __future__ import annotations

import argparse
from pathlib import Path

from tools.cli.dto import CLIContextDTO, CLIExitCode
from tools.cli.registry import CLICommandRegistry

"""Main CLI Application Driver for EAOS Human API."""


class EAOSCLIApp:
    """Human API CLI Driver."""

    def __init__(self) -> None:
        self.registry = CLICommandRegistry()

    def run(self, argv: list[str] | None = None) -> int:
        parser = argparse.ArgumentParser(
            prog="eaos",
            description="EAOS Enterprise Human API CLI",
        )
        parser.add_argument(
            "command",
            nargs="?",
            default="doctor",
            help="Command to run e.g. doctor, validate",
        )
        parser.add_argument(
            "--workspace",
            default=str(Path.cwd()),
            help="Workspace root path",
        )
        parser.add_argument(
            "--format",
            choices=["console", "json", "markdown"],
            default="console",
            help="Output format",
        )
        parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

        args = parser.parse_args(argv)

        ctx = CLIContextDTO(
            workspace_root=args.workspace,
            verbose=args.verbose,
            output_format=args.format,
        )

        cmd = self.registry.get_command(args.command)
        if not cmd:
            print(f"Unknown command: '{args.command}'")
            print("Available commands:")
            for c in self.registry.list_commands():
                print(f"  {c.command_name:<15} - {c.help_text}")
            return CLIExitCode.CONFIG_ERROR

        exit_code = cmd.execute(ctx)
        return int(exit_code)
