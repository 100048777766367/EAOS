import uuid

from packages.ai_agent.domain.models import AIAgentProfile

"""Application use cases for AI Agent Task Orchestration."""


class OrchestrateAgentTaskUseCase:
    """Use case assigning tasks to autonomous AI Agent."""

    def execute(self, role: str, model_name: str) -> AIAgentProfile:
        """Provisions an active AI Agent instance."""
        ag_id = f"AGT-{uuid.uuid4().hex[:8].upper()}"
        return AIAgentProfile(
            agent_id=ag_id,
            role=role,
            model_name=model_name,
            temperature=0.2,
            status="READY",
        )
