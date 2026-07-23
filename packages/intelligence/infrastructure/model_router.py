"""FinOps AI Model Router and cost/latency optimizer for EAOS intelligence."""

from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class ModelRoutingDecision(BaseModel):
    """Value object representing the routing decision for an AI task."""

    model_config = ConfigDict(frozen=True)

    selected_model: str
    reasoning_complexity: str
    estimated_cost_usd: float
    provider: str


class FinOpsModelRouter:
    """Dynamic FinOps model router optimizing LLM selection by cost and SLA."""

    HIGH_COMPLEXITY_KEYWORDS: ClassVar[set[str]] = {
        "architecture",
        "proof",
        "refactor",
        "optimize",
        "analysis",
        "reasoning",
    }

    def route_task(
        self,
        prompt: str,
        max_budget_usd: float = 0.05,
        max_latency_ms: int = 1000,
    ) -> ModelRoutingDecision:
        """Analyzes task prompt and routes to optimal LLM model within budget."""
        words = set(prompt.lower().split())
        has_high_complexity = bool(words.intersection(self.HIGH_COMPLEXITY_KEYWORDS))
        prompt_len = len(prompt)

        if max_budget_usd <= 0.001 or (prompt_len < 50 and not has_high_complexity):
            return ModelRoutingDecision(
                selected_model="ollama/llama3",
                reasoning_complexity="LOW",
                estimated_cost_usd=0.000,
                provider="Ollama-Local",
            )

        if has_high_complexity or prompt_len > 500:
            if max_budget_usd >= 0.02:
                return ModelRoutingDecision(
                    selected_model="claude-3-5-sonnet",
                    reasoning_complexity="HIGH",
                    estimated_cost_usd=0.015,
                    provider="Anthropic",
                )
            return ModelRoutingDecision(
                selected_model="deepseek/deepseek-r1",
                reasoning_complexity="HIGH",
                estimated_cost_usd=0.004,
                provider="DeepSeek",
            )

        return ModelRoutingDecision(
            selected_model="gpt-4o-mini",
            reasoning_complexity="MEDIUM",
            estimated_cost_usd=0.001,
            provider="OpenAI",
        )
