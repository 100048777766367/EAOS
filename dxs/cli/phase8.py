from __future__ import annotations

import sys
from pathlib import Path

from dxs.evolution.service import EvolutionService

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    """Run the Phase 8 self-diagnostics command."""
    service = EvolutionService()

    print("=" * 72)
    print("EAOS — DXS PHASE 8")
    print("=" * 72)

    capabilities = service.discover(ROOT)

    print("")
    print("[CAPABILITY DISCOVERY]")

    for capability in capabilities:
        status = "PASS" if capability.available else "FAIL"
        print(f"[{status}] {capability.name}: {capability.source}")

    health = service.health(capabilities)

    print("")
    print("[HEALTH MODEL]")
    print(f"Status: {health.status.value}")

    for check in health.checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"[{status}] {check.name}: {check.detail}")

    readiness = service.migration_readiness(
        health=health,
        contract_compatible=True,
    )

    print("")
    print("[MIGRATION READINESS]")
    print(f"Ready: {readiness.ready}")

    for blocker in readiness.blockers:
        print(f"[BLOCKER] {blocker}")

    for item in readiness.evidence:
        print(f"[EVIDENCE] {item}")

    evidence = service.evidence(
        ROOT,
        capabilities=capabilities,
        health=health,
        readiness=readiness,
    )

    print("")
    print("[EVOLUTIONARY EVIDENCE]")
    print(f"Repository: {evidence.repository_root}")
    print(f"Capabilities: {evidence.capability_count}")
    print(f"Files observed: {evidence.files_observed}")
    print(f"Healthy: {evidence.healthy}")
    print(f"Migration ready: {evidence.migration_ready}")

    print("=" * 72)

    return 0 if health.status.value == "healthy" else 1


if __name__ == "__main__":
    raise SystemExit(main())
