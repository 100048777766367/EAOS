from __future__ import annotations

from typing import Protocol, runtime_checkable

from tools.cli.dto import CLIContextDTO, CLIExitCode

"""Base Command Protocol for EAOS CLI."""


@runtime_checkable
class BaseCLICommand(Protocol):
    """Protocol defining the contract for all CLI commands."""

    command_name: str
    help_text: str

    def execute(self, ctx: CLIContextDTO) -> CLIExitCode: ...
