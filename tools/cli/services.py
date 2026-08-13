"""Application Services bridging CLI to Domain Engines."""

from __future__ import annotations

import asyncio
import subprocess
from pathlib import Path

import tools.validate.architecture_validator as val_mod
from tools.cli.dto import CLIContextDTO, CLIExitCode
from tools.doctor.engine import EAOSDoctorEngine
from tools.doctor.reporters.console_reporter import ConsoleReporter
from tools.doctor.reporters.json_reporter import JSONReporter
from tools.doctor.reporters.markdown_reporter import MarkdownReporter


class DoctorCLIService:
    """Application service for running Doctor via CLI."""

    def run_doctor(self, ctx: CLIContextDTO) -> CLIExitCode:
        root = Path(ctx.workspace_root)
        engine = EAOSDoctorEngine(workspace_root=root)
        report = engine.diagnose_system()

        if ctx.output_format == "json":
            out = JSONReporter().render(report)
        elif ctx.output_format == "markdown":
            out = MarkdownReporter().render(report)
        else:
            out = ConsoleReporter().render(report)

        print(out)

        if report.status == "READY":
            has_warns = any(c.status == "WARN" for c in report.checks)
            if has_warns:
                return CLIExitCode.WARNING
            return CLIExitCode.HEALTHY

        return CLIExitCode.FAILED


class ValidateCLIService:
    """Application service for running Architecture Validator."""

    def run_validation(self, ctx: CLIContextDTO) -> CLIExitCode:
        root = Path(ctx.workspace_root)

        # Directly import the ArchitectureValidator class from the module
        validator_cls = getattr(val_mod, "ArchitectureValidator", None)
        if validator_cls is None:
            print("Error: ArchitectureValidator class missing")
            return CLIExitCode.INTERNAL_ERROR
        validator = validator_cls(root)

        # Use the explicit validate_architecture method if available
        val_method = getattr(validator, "validate_architecture", None)
        if val_method is None:
            print("Error: validate_architecture method missing")
            return CLIExitCode.INTERNAL_ERROR

        report = val_method()
        compliant = getattr(report, "passed", True)  # Adjusted attribute name
        violations = getattr(report, "errors", [])

        status_str = "PASS" if compliant else "FAIL"
        print(f"Architecture Validator: {status_str}")
        print(f"Violations: {len(violations)}")

        if compliant:
            return CLIExitCode.HEALTHY
        return CLIExitCode.FAILED


class RuntimeCLIService:
    """Application service for managing production daemon runtime."""

    def run_status(self, ctx: CLIContextDTO) -> CLIExitCode:
        root = Path(ctx.workspace_root)
        cmd = [
            "docker",
            "ps",
            "--format",
            "table {{.Names}}\t{{.Status}}\t{{.Ports}}",
        ]
        try:
            res = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True)
            print("EAOS Production Daemon Status:")
            print(res.stdout or "No containers running.")
            return CLIExitCode.HEALTHY
        except Exception as err:
            print(f"Failed to check runtime status: {err}")
            return CLIExitCode.INTERNAL_ERROR


class BenchmarkCLIService:
    """Application service for running Swarm & RAG Benchmarks."""

    def run_benchmark_suite(self, ctx: CLIContextDTO) -> CLIExitCode:
        from tools.benchmark.swarm_rag_benchmark_adapter import (
            SwarmRAGBenchmarkAdapter,
        )
        from tools.chaos.dto import ChaosFaultConfig, FaultType
        from tools.chaos.swarm_rag_chaos_adapter import (
            SwarmRAGChaosAdapter,
        )

        async def _async_run() -> None:
            print("=== EAOS SWARM & RAG CHAOS BENCHMARK SUITE ===")

            chaos_adapter = SwarmRAGChaosAdapter()
            fault_cfg = ChaosFaultConfig(
                fault_type=FaultType.LLM_RATE_LIMIT_429,
                target_component="GeminiCloudProvider",
            )
            report = await chaos_adapter.inject_fault_and_verify(fault_cfg)
            print(f"Chaos Test ID     : {report.experiment_id}")
            print(f"Fault Injected    : {report.fault_config.fault_type}")
            print(f"Fallback Verified : {report.fallback_triggered}")
            print(f"Recovery Latency  : {report.recovery_latency_ms} ms")

            bench_adapter = SwarmRAGBenchmarkAdapter()
            metrics = await bench_adapter.run_benchmark(iterations=20)
            print("\n--- Performance Metrics ---")
            print(f"Throughput        : {metrics.throughput_ops_sec} ops/sec")
            print(f"P50 Latency       : {metrics.p50_latency_ms} ms")
            print(f"P95 Latency       : {metrics.p95_latency_ms} ms")
            print(f"P99 Latency       : {metrics.p99_latency_ms} ms")
            print(f"RAG Precision     : {metrics.rag_precision_score * 100}%")

        asyncio.run(_async_run())
        return CLIExitCode.HEALTHY
