from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

"""Chaos Engineering and Benchmark DTOs (Option 2)."""


class FaultType(StrEnum):
    """Fault types for Swarm and RAG Chaos Engineering."""

    DATABASE_DISCONNECT = "DATABASE_DISCONNECT"
    NEO4J_TIMEOUT = "NEO4J_TIMEOUT"
    LLM_RATE_LIMIT_429 = "LLM_RATE_LIMIT_429"
    LLM_LATENCY_SPIKE = "LLM_LATENCY_SPIKE"
    SWARM_AGENT_FAILURE = "SWARM_AGENT_FAILURE"


class ChaosFaultConfig(BaseModel):
    """Configuration for chaos fault injection."""

    model_config = ConfigDict(frozen=True)

    fault_type: FaultType = Field(..., description="Target fault type")
    target_component: str = Field(..., description="Target component")
    duration_sec: float = Field(default=1.0, description="Duration")


class ChaosExperimentReport(BaseModel):
    """Report produced by chaos experiment execution."""

    model_config = ConfigDict(frozen=True)

    experiment_id: str = Field(..., description="Unique experiment ID")
    fault_config: ChaosFaultConfig
    fallback_triggered: bool = Field(default=True)
    system_recovered: bool = Field(default=True)
    recovery_latency_ms: float = Field(default=0.0)
    evidence_summary: str = Field(default="")


class BenchmarkMetricDTO(BaseModel):
    """Metric DTO for Swarm and RAG performance benchmark."""

    model_config = ConfigDict(frozen=True)

    benchmark_id: str = Field(..., description="Benchmark run ID")
    throughput_ops_sec: float = Field(default=0.0)
    p50_latency_ms: float = Field(default=0.0)
    p95_latency_ms: float = Field(default=0.0)
    p99_latency_ms: float = Field(default=0.0)
    rag_precision_score: float = Field(default=1.0)
    total_iterations: int = Field(default=10)
