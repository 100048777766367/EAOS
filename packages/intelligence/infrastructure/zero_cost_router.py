from pydantic import BaseModel, ConfigDict

"""Zero-Cost FinOps Router enforcing $0 USD AI inference budget."""


class ZeroCostRoutingResultDTO(BaseModel):
    """Value object representing a zero-cost model routing decision."""

    model_config = ConfigDict(frozen=True)

    task_prompt: str
    selected_provider: str
    selected_model: str
    estimated_cost_usd: float = 0.0
    is_zero_cost: bool = True


class ZeroCostModelRouter:
    """FinOps Router strictly enforcing $0 USD operational cost."""

    def route_zero_cost_task(self, prompt: str, force_local_ollama: bool = True) -> ZeroCostRoutingResultDTO:
        """Routes task to local Ollama LLM or free-tier cloud provider."""
        p_lower = prompt.lower()

        if force_local_ollama or "code" in p_lower:
            provider = "OLLAMA_LOCAL"
            model = "qwen2.5-coder:7b"
        elif "reason" in p_lower or "deep" in p_lower:
            provider = "OLLAMA_LOCAL"
            model = "deepseek-r1:8b"
        else:
            provider = "GROQ_FREE_TIER"
            model = "llama-3.3-70b-versatile"

        return ZeroCostRoutingResultDTO(
            task_prompt=prompt,
            selected_provider=provider,
            selected_model=model,
            estimated_cost_usd=0.0,
            is_zero_cost=True,
        )


if __name__ == "__main__":
    router = ZeroCostModelRouter()
    res = router.route_zero_cost_task("Thiet ke Bounded Context CRM")
    print(f"✔ Selected Provider: {res.selected_provider}")
    print(f"✔ Selected Model   : {res.selected_model}")
    print(f"✔ Estimated Cost   : ${res.estimated_cost_usd} USD (100% Free)")
