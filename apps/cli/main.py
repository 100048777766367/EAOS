import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="EAOS - Enterprise Architecture Operating System CLI")
console = Console()


@app.command()
def version() -> None:
    """Hiển thị phiên bản EAOS CLI."""
    console.print("[bold green]EAOS CLI[/bold green] - Phiên bản [cyan]0.1.0[/cyan]")


@app.command()
def doctor() -> None:
    """Chạy kiểm tra sức khỏe hệ thống."""
    console.print("[bold yellow]Bắt đầu chẩn đoán hệ thống EAOS...[/bold yellow]\n")
    try:
        from tools.doctor import main as doc
        doc.run_diagnostics()
    except Exception as e:
        console.print(f"[bold red]Lỗi khi chạy chẩn đoán:[/bold red] {e}")


@app.command()
def init() -> None:
    """Khởi tạo EAOS Workspace."""
    console.print("[bold green]Khởi tạo EAOS Workspace thành công![/bold green]")


@app.command()
def info() -> None:
    """Hiển thị thông tin kiến trúc."""
    table = Table(title="Thông tin Hệ thống EAOS")
    table.add_column("Hạng mục", style="cyan")
    table.add_column("Giá trị", style="magenta")
    table.add_row("Tên hệ thống", "Enterprise Architecture Operating System")
    table.add_row("Kiến trúc", "Modular Monolith")
    table.add_row("Trạng thái", "Sprint 1 — Core Foundation")
    console.print(table)


# --- LỆNH KIỂM TOÁN KIẾN TRÚC TỐI CAO (SPRINT A - SỬA LỖI TYPER) ---


@app.command()
def validate() -> None:
    """Chạy kiểm toán và ép buộc tuân thủ Hiến pháp kiến trúc."""
    console.print(
        "[bold blue]Khởi chạy EAOS Architecture Validator...[/bold blue]\n"
    )

    from pathlib import Path

    from tools.validate.architecture_validator import ArchitectureValidator

    root_dir = Path(__file__).resolve().parent.parent.parent
    validator = ArchitectureValidator(root_dir)
    passed = validator.run_all_checks()

    if passed:
        console.print(
            "[bold green]✔ KIẾN TRÚC ĐẠT CHUẨN KIỂM TOÁN TUYỆT ĐỐI.[/bold green]"
        )
    else:
        console.print("[bold red]✘ PHÁT HIỆN VI PHẠM KIẾN TRÚC TỐI CAO:[/bold red]\n")
        for violation in validator.violations:
            console.print(f"  • {violation}", style="yellow")
        raise typer.Exit(code=1)


# --- LỆNH TỰ ĐỘNG SINH ĐỒ THỊ PHỤ THUỘC (SPRINT B - SỬA LỖI TYPER) ---


@app.command()
def graph() -> None:
    """Tự động phân tích mã nguồn và xuất bản đồ đồ thị phụ thuộc."""
    console.print(
        "[bold blue]Khởi chạy EAOS Dependency Graph Generator...[/bold blue]\n"
    )

    from pathlib import Path

    from tools.graph.dependency_graph_generator import DependencyGraphGenerator

    root_dir = Path(__file__).resolve().parent.parent.parent
    generator = DependencyGraphGenerator(root_dir)
    success = generator.generate()

    if success:
        console.print(
            "[bold green]✔ TỰ ĐỘNG XUẤT ĐỒ THỊ PHỤ THUỘC THÀNH CÔNG.[/bold green]"
        )
        console.print(
            "  • Đồ thị JSON: [cyan]"
            "generated/architecture/dependency_graph.json[/cyan]"
        )
        console.print(
            "  • Sơ đồ Mermaid: [cyan]"
            "generated/architecture/dependency_graph.md[/cyan]"
        )
        console.print(
            "  • Sơ đồ Graphviz: [cyan]"
            "generated/architecture/dependency_graph.dot[/cyan]"
        )
    else:
        console.print("[bold red]✘ LỖI KHI TẠO ĐỒ THỊ PHỤ THUỘC.[/bold red]")
        raise typer.Exit(code=1)


# --- LỆNH ĐO LƯỜNG CHỈ SỐ CHẤT LƯỢNG KIẾN TRÚC (SPRINT C - PHASE 2) ---


@app.command()
def metrics() -> None:
    """Đo lường và tính toán chỉ số chất lượng kiến trúc hằng ngày."""
    console.print(
        "[bold blue]Khởi chạy EAOS Architecture Metrics Calculator...[/bold blue]\n"
    )

    from pathlib import Path
    from tools.metrics.architecture_metrics_calculator import (
        ArchitectureMetricsCalculator,
    )

    root_dir = Path(__file__).resolve().parent.parent.parent
    calculator = ArchitectureMetricsCalculator(root_dir)
    success = calculator.calculate_all()

    if success:
        console.print(
            "[bold green]✔ TÍNH TOÁN CHỈ SỐ KIẾN TRÚC THÀNH CÔNG.[/bold green]"
        )
        console.print(
            "  • Điểm chất lượng: "
            f"[bold cyan]{calculator.architecture_score}/100[/bold cyan]"
        )
        console.print(
            "  • Chỉ số JSON: [cyan]"
            "generated/architecture/architecture_metrics.json[/cyan]"
        )
        console.print(
            "  • Báo cáo MD: [cyan]"
            "generated/architecture/architecture_metrics.md[/cyan]"
        )
    else:
        console.print("[bold red]✘ LỖI KHI ĐO LƯỜNG CHỈ SỐ KIẾN TRÚC.[/bold red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
