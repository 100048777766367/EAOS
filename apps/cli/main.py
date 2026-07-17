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

if __name__ == "__main__":
    app()