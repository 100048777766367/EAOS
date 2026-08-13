"""Application use cases for Swarm Intelligence Orchestration."""

import sys
import uuid
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

from packages.swarm_intelligence.domain.models import (  # noqa: E402
    InsectRoleEnum,
    PheromoneSignalVO,
    SwarmAgentProfile,
)


class OrchestrateSwarmTaskUseCase:
    """Use case coordinating biomimetic multi-agent swarm execution."""

    def execute(self, role: InsectRoleEnum, topic: str) -> tuple[SwarmAgentProfile, PheromoneSignalVO]:
        """Spawns swarm agent and emits stigmergic pheromone signal."""
        ag_id = f"SWARM-{uuid.uuid4().hex[:8].upper()}"
        sig_id = f"PHR-{uuid.uuid4().hex[:8].upper()}"

        profile = SwarmAgentProfile(
            agent_id=ag_id,
            role=role,
            specialization=f"Autonomous {role.value} Operator",
            status="ACTIVE",
        )
        signal = PheromoneSignalVO(
            signal_id=sig_id,
            origin_role=role,
            intensity=1.0,
            topic_target=topic,
        )
        return profile, signal


if __name__ == "__main__":
    uc = OrchestrateSwarmTaskUseCase()
    prof, sig = uc.execute(InsectRoleEnum.SPIDER_WEAVER, "knowledge_graph")
    print(f"✔ Swarm Agent Spawned: {prof.agent_id} ({prof.role.value})")
    print(f"✔ Pheromone Signal Emitted: {sig.signal_id} -> {sig.topic_target}")
