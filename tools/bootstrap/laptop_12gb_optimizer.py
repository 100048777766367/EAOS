from pydantic import BaseModel, ConfigDict

"""12GB RAM Laptop Hardware Optimizer & Lightweight Mode Configurator."""


class HardwareOptimizationProfileDTO(BaseModel):
    """Value object representing settings for 12GB RAM laptop."""

    model_config = ConfigDict(frozen=True)

    docker_required: bool = False
    database_engine: str = "SQLITE_WAL_IN_PROCESS"
    cache_engine: str = "IN_MEMORY_SPLAY_TREE"
    storage_engine: str = "LOCAL_FILE_SYSTEM"
    recommended_llm: str = "qwen2.5-coder:3b OR GROQ_FREE_API"
    expected_ram_usage_mb: int = 300


class Laptop12GBOptimizer:
    """Optimizer configuring EAOS for 12GB RAM Dell Inspiron laptop."""

    def generate_lightweight_config(
        self,
    ) -> HardwareOptimizationProfileDTO:
        """Generates zero-Docker ultra-lightweight profile for 12GB RAM."""
        return HardwareOptimizationProfileDTO(
            docker_required=False,
            database_engine="SQLITE_WAL_IN_PROCESS",
            cache_engine="IN_MEMORY_SPLAY_TREE",
            storage_engine="LOCAL_FILE_SYSTEM",
            recommended_llm="qwen2.5-coder:3b (Local) / Groq Free API",
            expected_ram_usage_mb=300,
        )


if __name__ == "__main__":
    optimizer = Laptop12GBOptimizer()
    prof = optimizer.generate_lightweight_config()
    print("====================================================")
    print(" EAOS 12GB RAM LAPTOP HARDWARE OPTIMIZATION REPORT  ")
    print("====================================================")
    print(f"✔ Docker Required      : {prof.docker_required} (NO DOCKER NEEDED)")
    print(f"✔ Database Engine    : {prof.database_engine}")
    print(f"✔ Cache Engine       : {prof.cache_engine}")
    print(f"✔ Storage Engine     : {prof.storage_engine}")
    print(f"✔ Recommended LLM    : {prof.recommended_llm}")
    print(f"✔ Total EAOS RAM Needed: ~{prof.expected_ram_usage_mb} MB")
    print("====================================================")
