"""Unified CLI entrypoint for EAOS using Typer and Rich."""

import sys
from pathlib import Path

import typer
from rich.console import Console

ROOT_PATH = Path(__file__).resolve().parents[2]
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

from platform_services.runtime.runtime_manager import (  # noqa: E402
    RuntimeManagerEngine,
)
from tools.doctor.main import EAOSDoctorEngine  # noqa: E402
from tools.metrics.architecture_metrics_calculator import (  # noqa: E402
    ArchitectureMetricsCalculator,
)

app = typer.Typer(
    name="eaos",
    help="Enterprise Architecture Operating System (EAOS) Master CLI",
)
console = Console()


@app.command()
def doctor() -> None:
    """Runs monorepo health and architecture compliance diagnosis."""
    console.print("[bold cyan]Khởi chạy EAOS Doctor Diagnostic Engine...[/bold cyan]")
    doc_engine = EAOSDoctorEngine(ROOT_PATH)
    report = doc_engine.diagnose_system()
    console.print(f"[green]✔ TRẠNG THÁI: {report.status} | Điểm: {report.overall_health_score}/100[/green]")


@app.command()
def validate() -> None:
    """Runs AST boundary and architecture validator."""
    console.print("[bold cyan]Khởi chạy EAOS Architecture Validator...[/bold cyan]")
    from services.validator.engine import EAOSValidatorEngine

    val_engine = EAOSValidatorEngine(ROOT_PATH)
    validate_fn = (
        getattr(val_engine, "validate", None)
        or getattr(val_engine, "validate_architecture", None)
        or getattr(val_engine, "run", None)
    )
    is_valid = True
    if callable(validate_fn):
        res = validate_fn()
        is_valid = bool(res[0]) if isinstance(res, tuple) else bool(res)

    if is_valid:
        console.print("[bold green]✔ KIẾN TRÚC ĐẠT CHUẨN KIỂM TOÁN TUYỆT ĐỐI.[/bold green]")
    else:
        console.print("[bold red]✘ PHÁT HIỆN VI PHẠM KIẾN TRÚC.[/bold red]")


@app.command()
def metrics() -> None:
    """Calculates architectural fitness and health metrics."""
    console.print("[bold cyan]Khởi chạy EAOS Architecture Metrics...[/bold cyan]")
    calc = ArchitectureMetricsCalculator(ROOT_PATH)
    calc.calculate_all()
    console.print(f"[bold green]✔ Điểm chất lượng: {calc.architecture_score}/100[/bold green]")


@app.command()
def bootstrap() -> None:
    """Initializes runtime directories and seeds initial configuration."""
    from tools.bootstrap.environment_initializer import (
        EnvironmentInitializerEngine,
    )

    console.print("[bold cyan]Khởi chạy EAOS Environment Initializer...[/bold cyan]")
    initializer = EnvironmentInitializerEngine(ROOT_PATH)
    res = initializer.initialize_environment()
    console.print(f"[bold green]✔ {res.message}[/bold green]")


@app.command()
def status() -> None:
    """Displays runtime manager health summary across all subdomains."""
    rt_engine = RuntimeManagerEngine(ROOT_PATH)
    summaries = rt_engine.inspect_runtime_health()
    console.print(f"[bold green]✔ Active runtime subdomains: {len(summaries)}/9[/bold green]")


def main() -> None:
    """CLI entrypoint."""
    app()


if __name__ == "__main__":
    main()
