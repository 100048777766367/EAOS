from __future__ import annotations

import asyncio
import sys

from agents.orchestrator import AutonomousAgentSwarm

"""Executable entrypoint for EAOS Agent Application."""


def main() -> None:
    """Main agent application execution entrypoint."""
    goal = sys.argv[1] if len(sys.argv) > 1 else "Autonomous System Health Audit"
    print("=== EAOS Agent Application Driver ===")
    print(f"Executing goal: '{goal}'")

    swarm = AutonomousAgentSwarm()
    results = asyncio.run(swarm.run_full_swarm(goal, mode="AUTO"))

    print(f"✔ Completed {len(results)} agent steps successfully.")


if __name__ == "__main__":
    main()
