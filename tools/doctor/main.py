from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tools.doctor.engine import EAOSDoctorEngine
from tools.doctor.reporters.console_reporter import ConsoleReporter
from tools.doctor.reporters.json_reporter import JSONReporter
from tools.doctor.reporters.markdown_reporter import MarkdownReporter

"""CLI Entrypoint for EAOS Enterprise Doctor."""


def main() -> None:
    """CLI main function for doctor."""
    parser = argparse.ArgumentParser(description="EAOS Enterprise Doctor")
    parser.add_argument(
        "--workspace",
        default=str(Path.cwd()),
        help="Workspace root directory",
    )
    parser.add_argument(
        "--format",
        choices=["console", "json", "markdown"],
        default="console",
        help="Report output format",
    )
    args = parser.parse_args()

    root = Path(args.workspace).resolve()
    engine = EAOSDoctorEngine(workspace_root=root)
    report = engine.diagnose_system()

    if args.format == "json":
        print(JSONReporter().render(report))
    elif args.format == "markdown":
        print(MarkdownReporter().render(report))
    else:
        print(ConsoleReporter().render(report))

    if report.status != "READY":
        sys.exit(1)


if __name__ == "__main__":
    main()
