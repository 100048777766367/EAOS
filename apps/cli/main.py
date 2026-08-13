from __future__ import annotations

import sys

from tools.cli.app import EAOSCLIApp

"""Executable entrypoint for EAOS CLI Application."""


def main() -> None:
    """Main CLI application entrypoint."""
    app = EAOSCLIApp()
    exit_code = app.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
