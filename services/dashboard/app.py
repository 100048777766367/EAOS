import json
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from services.validator.engine import EAOSValidatorEngine

app = typer.Typer(help="EAOS - Enterprise Architecture Operating System CLI")
console = Console()

ROOT_PATH = Path(__file__).resolve().parent.parent.parent
OUTPUT_PATH = ROOT_PATH / "generated" / "report.json"


@app.command()
def validate() -> None:
    """Chạy kiểm toán ranh giới và biểu quyết sáp nhập vĩnh cửu."""
    console.print("[bold blue]Khởi chạy EAOS Architecture Validator...[/bold blue]\n")

    engine = EAOSValidatorEngine(ROOT_PATH)
    report = engine.run_validation()

    # Ghi nhận kết quả ra tệp generated/report.json
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report.model_dump(), f, indent=2, ensure_ascii=False)

    if report.overall_passed:
        title = Text("✔ HIẾN PHÁP KIẾN TRÚC EAOS HỢP CHUẨN", style="bold green")
        panel = Panel(
            "Tất cả ranh giới phụ thuộc và hồ sơ đạt chất lượng tuyệt đối.",
            title=title,
            border_style="green",
        )
    else:
        title = Text("✘ PHÁT HIỆN VI PHẠN KIẾN PHÁP", style="bold red")
        panel = Panel(
            "Phát hiện lỗi không tuân thủ. Vui lòng kiểm duyệt chẩn đoán.",
            title=title,
            border_style="red",
        )

    console.print(panel)
    console.print("\n[bold]Bảng Đánh Giá Luật:[/bold]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Tên Quy Tắc", style="cyan", width=30)
    table.add_column("Kết Quả", width=12, justify="center")
    table.add_column("Thông Điệp", style="white")

    for res in report.results:
        status = "[bold green]ĐẠT[/bold green]" if res.passed else "[bold red]LỖI[/bold red]"
        table.add_row(res.rule_name, status, res.message)

    console.print(table)

    for res in report.results:
        if not res.passed and res.details:
            console.print(f"\n[bold red]Chi tiết lỗi: {res.rule_name}[/bold red]")
            for detail in res.details:
                console.print(f"  • {detail}", style="yellow")

    if not report.overall_passed:
        raise typer.Exit(code=1)


@app.command()
def graph() -> None:
    """Tự động phân tích mã nguồn và sinh đồ thị phụ thuộc (Mermaid)."""
    console.print("[bold blue]Sinh đồ thị phụ thuộc EAOS...[/bold blue]\n")
    from libs.validation.checker import ASTBoundaryChecker

    checker = ASTBoundaryChecker(ROOT_PATH)
    graph_data = checker.scan_dependencies()

    table = Table(title="Đồ thị phụ thuộc của Packages")
    table.add_column("Package gốc", style="cyan")
    table.add_column("Phụ thuộc vào", style="green")

    for pkg, deps in graph_data.items():
        table.add_row(pkg, ", ".join(deps) or "Không")

    console.print(table)


@app.command()
def metrics() -> None:
    """Đo lường chỉ số chất lượng Robert C. Martin."""
    console.print("[bold blue]Tính toán chỉ số Instability...[/bold blue]\n")
    from libs.validation.checker import ASTBoundaryChecker

    checker = ASTBoundaryChecker(ROOT_PATH)
    graph_data = checker.scan_dependencies()

    table = Table(title="Chỉ số Instability (I) hằng ngày")
    table.add_column("Gói", style="cyan")
    table.add_column("Ca (In)", justify="center")
    table.add_column("Ce (Out)", justify="center")
    table.add_column("Instability (I)", justify="center", style="yellow")

    packages = list(graph_data.keys())
    for pkg in packages:
        ce = len(graph_data[pkg])
        ca = sum(1 for other in packages if pkg in graph_data[other])
        i = ce / (ca + ce) if (ca + ce) > 0 else 0.0
        table.add_row(pkg, str(ca), str(ce), f"{i:.4f}")

    console.print(table)


if __name__ == "__main__":
    app()
