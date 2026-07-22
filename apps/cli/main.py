from datetime import UTC, datetime

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
    table.add_row("Trạng thái", "Phase 4 — Enterprise Ecosystem")
    console.print(table)


# --- LỆNH KIỂM TOÁN KIẾN TRÚC TỐI CAO (SPRINT A - PHASE 2) ---


@app.command()
def validate() -> None:
    """Chạy kiểm toán và ép buộc tuân thủ Hiến pháp kiến trúc."""
    console.print("[bold blue]Khởi chạy EAOS Architecture Validator...[/bold blue]\n")

    from pathlib import Path

    from tools.validate.architecture_validator import ArchitectureValidator

    root_dir = Path(__file__).resolve().parent.parent.parent
    validator = ArchitectureValidator(root_dir)
    passed = validator.run_all_checks()

    if passed:
        console.print("[bold green]✔ KIẾN TRÚC ĐẠT CHUẨN KIỂM TOÁN TUYỆT ĐỐI.[/bold green]")
    else:
        console.print("[bold red]✘ PHÁT HIỆN VI PHẠM KIẾN TRÚC TỐI CAO:[/bold red]\n")
        for violation in validator.violations:
            console.print(f"  • {violation}", style="yellow")
        raise typer.Exit(code=1)


# --- LỆNH TỰ ĐỘNG SINH ĐỒ THỊ PHỤ THUỘC (SPRINT B - PHASE 2) ---


@app.command()
def graph() -> None:
    """Tự động phân tích mã nguồn và xuất bản đồ đồ thị phụ thuộc."""
    console.print("[bold blue]Khởi chạy EAOS Dependency Graph Generator...[/bold blue]\n")

    from pathlib import Path

    from tools.graph.dependency_graph_generator import (
        DependencyGraphGenerator,
    )

    root_dir = Path(__file__).resolve().parent.parent.parent
    generator = DependencyGraphGenerator(root_dir)
    success = generator.generate()

    if success:
        console.print("[bold green]✔ TỰ ĐỘNG XUẤT ĐỒ THỊ PHỤ THUỘC THÀNH CÔNG.[/bold green]")
        console.print("  • Đồ thị JSON: [cyan]generated/architecture/dependency_graph.json[/cyan]")
        console.print("  • Sơ đồ Mermaid: [cyan]generated/architecture/dependency_graph.md[/cyan]")
        console.print("  • Sơ đồ Graphviz: [cyan]generated/architecture/dependency_graph.dot[/cyan]")
    else:
        console.print("[bold red]✘ LỖI KHI TẠO ĐỒ THỊ PHỤ THUỘC.[/bold red]")
        raise typer.Exit(code=1)


# --- LỆNH ĐO LƯỜNG CHỈ SỐ CHẤT LƯỢNG KIẾN TRÚC (SPRINT C - PHASE 2) ---


@app.command()
def metrics() -> None:
    """Đo lường và tính toán chỉ số chất lượng kiến trúc hằng ngày."""
    console.print("[bold blue]Khởi chạy EAOS Architecture Metrics Calculator...[/bold blue]\n")

    from pathlib import Path

    from tools.metrics.architecture_metrics_calculator import (
        ArchitectureMetricsCalculator,
    )

    root_dir = Path(__file__).resolve().parent.parent.parent
    calculator = ArchitectureMetricsCalculator(root_dir)
    success = calculator.calculate_all()

    if success:
        console.print("[bold green]✔ TÍNH TOÁN CHỈ SỐ KIẾN TRÚC THÀNH CÔNG.[/bold green]")
        console.print(f"  • Điểm chất lượng: [bold cyan]{calculator.architecture_score}/100[/bold cyan]")
        console.print("  • Chỉ số JSON: [cyan]generated/architecture/architecture_metrics.json[/cyan]")
        console.print("  • Báo cáo MD: [cyan]generated/architecture/architecture_metrics.md[/cyan]")
    else:
        console.print("[bold red]✘ LỖI KHI ĐO LƯỜNG CHỈ SỐ KIẾN TRÚC.[/bold red]")
        raise typer.Exit(code=1)


# --- CỖ MÁY THỜI GIAN KIẾN TRÚC (SPRINT E - PHASE 2) ---


@app.command()
def time_machine(
    action: str = typer.Argument("list", help="record / list / compare"),
    param1: str = typer.Argument(None, help="Mã Snapshot A / Commit Hash"),
    param2: str = typer.Argument(None, help="Mã Snapshot B"),
) -> None:
    """Điều phối cỗ máy thời gian lưu vết lịch sử kiến trúc EAOS."""
    from pathlib import Path

    from tools.time_machine.time_machine import ArchitectureTimeMachine

    root_dir = Path(__file__).resolve().parent.parent.parent
    tm = ArchitectureTimeMachine(root_dir)

    if action == "record":
        if not param1:
            console.print("[bold red]Lỗi: Cung cấp Commit Hash.[/bold red]")
            raise typer.Exit(code=1)
        console.print(f"[bold blue]Chụp Snapshot: {param1}...[/bold blue]")
        tm.record_snapshot(param1)
        console.print("[bold green]✔ ĐÃ GHI NHẬN SNAPSHOT KIẾN TRÚC.[/bold green]")

    elif action == "compare":
        if not param1 or not param2:
            console.print("[bold red]Lỗi: Cung cấp đủ 2 mã Snapshot.[/bold red]")
            raise typer.Exit(code=1)
        console.print(f"[bold blue]Đối chiếu: {param1} ──► {param2}...[/bold blue]\n")
        try:
            diff = tm.compare_snapshots(param1, param2)

            table = Table(title=f"Báo cáo đối chiếu: {param1} vs {param2}")
            table.add_column("Hạng mục", style="cyan")
            table.add_column("Chi tiết biến đổi", style="yellow")

            diff_score = f"{diff['score_diff']} điểm" if diff["score_diff"] <= 0 else f"+{diff['score_diff']} điểm"
            table.add_row("Biến động điểm số", diff_score)
            table.add_row("Gói bổ sung mới", ", ".join(diff["added_packages"]) or "Không")
            table.add_row("Gói bị loại bỏ", ", ".join(diff["removed_packages"]) or "Không")
            table.add_row("Vi phạm mới rò rỉ", ", ".join(diff["new_violations"]) or "Không")
            table.add_row(
                "Vi phạm đã vá lỗi",
                ", ".join(diff["resolved_violations"]) or "Không",
            )

            console.print(table)
        except ValueError as e:
            console.print(f"[bold red]Lỗi: {e}[/bold red]")
            # Sửa lỗi B904 bằng raise from e
            raise typer.Exit(code=1) from e

    else:
        # Mặc định: list
        console.print("[bold blue]Lịch sử các Snapshot kiến trúc:[/bold blue]\n")
        snapshots = tm.list_snapshots()
        if not snapshots:
            console.print("[yellow]Chưa có Snapshot nào được chụp.[/yellow]")
            return

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Mã Snapshot", style="cyan")
        table.add_column("Thời gian ghi", style="magenta")
        table.add_column("Điểm chất lượng", style="green")
        table.add_column("Số vi phạm", style="rose")

        for snap in snapshots:
            table.add_row(
                snap["snapshot_id"],
                snap["timestamp"][:19].replace("T", " "),
                f"{snap['architecture_score']}/100",
                str(len(snap["violations"])),
            )
        console.print(table)


# --- BỘ ĐIỀU PHỐI BẢN SAO SỐ (SPRINT F - PHASE 2) ---


@app.command()
def twin(
    proposal_file: str = typer.Argument(None, help="Đường dẫn tới tệp tin đề xuất (JSON)"),
) -> None:
    """Khởi chạy Digital Twin mô phỏng ảnh hưởng của đề xuất trước khi sáp nhập."""
    console.print("[bold blue]Khởi chạy EAOS Digital Twin Orchestrator...[/bold blue]\n")

    import json
    from pathlib import Path

    from tools.digital_twin.digital_twin import DigitalTwinOrchestrator

    root_dir = Path(__file__).resolve().parent.parent.parent

    if proposal_file and Path(proposal_file).exists():
        with open(proposal_file, encoding="utf-8") as f:
            proposal = json.load(f)
    else:
        console.print("[yellow]Cảnh báo: Không truyền tệp đề xuất. Chạy mặc định...[/yellow]")
        proposal = {
            "package_name": "eaos-finance",
            "layer": "infrastructure",
            "dependencies": ["packages.knowledge.domain"],
        }

    orchestrator = DigitalTwinOrchestrator(root_dir)
    result = orchestrator.evaluate_proposal(proposal)

    table = Table(title="Báo cáo Đánh giá Bản sao số (Digital Twin)")
    table.add_column("Chỉ số", style="cyan")
    table.add_column("Giá trị", style="yellow")

    status_color = "green" if result["status"] == "APPROVED" else "red"
    table.add_row(
        "Trạng thái Quyết định",
        f"[bold {status_color}]{result['status']}[/bold {status_color}]",
    )
    table.add_row("Điểm hiện tại", str(result["current_score"]))
    table.add_row("Điểm giả lập", str(result["simulated_score"]))
    table.add_row("Độ lệch điểm số", f"{result['score_delta']} điểm")
    table.add_row("Vi phạm giả lập", str(len(result["simulated_violations"])))
    table.add_row("Khuyến nghị chính", "\n".join(result["recommendations"]))

    console.print(table)


# --- ĐỘNG CƠ BIÊN DỊCH KIẾN TRÚC TỐI CAO (SPRINT G - SỬA LỖI TYPER) ---


@app.command()
def compile_spec(
    spec_file: str = typer.Argument(None, help="Đường dẫn tới tệp tin đặc tả (JSON)"),
) -> None:
    """Biên dịch toàn bộ đặc tả thành mã nguồn Python, Docker, và Terraform."""
    console.print("[bold blue]Khởi chạy EAOS Architecture Compiler...[/bold blue]\n")

    import json
    from pathlib import Path

    from engine.compiler.architecture_compiler import ArchitectureCompiler

    root_dir = Path(__file__).resolve().parent.parent.parent

    if spec_file and Path(spec_file).exists():
        with open(spec_file, encoding="utf-8") as f:
            spec = json.load(f)
    else:
        console.print("[yellow]Cảnh báo: Không truyền tệp đặc tả. Sử dụng 'billing'...[/yellow]")
        spec = {
            "capability_name": "billing",
            "description": "Enterprise Billing Capability",
            "database": "postgresql",
            "entities": [
                {
                    "name": "Invoice",
                    "fields": {
                        "id": "str",
                        "amount": "float",
                        "customer_id": "str",
                    },
                }
            ],
            "deployment": {
                "orchestration": "kubernetes",
                "iac": "terraform",
            },
        }

    compiler = ArchitectureCompiler(root_dir)
    success = compiler.compile_spec(spec)

    if success:
        console.print("[bold green]✔ BIÊN DỊCH KIẾN TRÚC THÀNH CÔNG.[/bold green]")
        console.print(f"  • Thư mục biên dịch: [cyan]generated/compiler/{spec['capability_name']}/[/cyan]")
        console.print("    - Domain Models: [cyan].../domain/models.py[/cyan]")
        console.print("    - Domain Ports: [cyan].../domain/ports.py[/cyan]")
        console.print("    - Infrastructure: [cyan].../infrastructure/[/cyan]")
        console.print("    - Dockerfile: [cyan].../deployment/Dockerfile[/cyan]")
        console.print("    - Terraform IaC: [cyan].../deployment/main.tf[/cyan]")
    else:
        console.print("[bold red]✘ LỖI KHI BIÊN DỊCH KIẾN TRÚC.[/bold red]")
        raise typer.Exit(code=1)


# --- ĐỘNG CƠ ĐIỀU PHỐI 3 VÒNG PHẢN HỒI LỒNG NHAU (SPRINT E - SỬA LỖI TYPER) ---


@app.command()
def loop(
    type_arg: str = typer.Argument("execution", help="execution / architecture / strategy"),
) -> None:
    """Kiểm toán tuân thủ ranh giới của 3 vòng phản hồi lồng nhau."""
    console.print("[bold blue]Khởi chạy EAOS Governance Loop Engine...[/bold blue]\n")

    from pathlib import Path

    from kernel.governance.loop_engine import GovernanceLoopEngine, LoopTrigger

    root_dir = Path(__file__).resolve().parent.parent.parent
    engine = GovernanceLoopEngine(root_dir)

    cadence_map = {
        "EXECUTION": "FAST (Minutes/Hours)",
        "ARCHITECTURE": "MEDIUM (Weeks/Months)",
        "STRATEGY": "SLOW (Years)",
    }
    loop_type = type_arg.upper()
    cadence = cadence_map.get(loop_type, "UNKNOWN")

    trigger = LoopTrigger(
        loop_type=loop_type,
        cadence=cadence,
        trigger_context=f"CLI trigger at {datetime.now(UTC).isoformat()}",
    )
    execution = engine.evaluate_loop(trigger)

    table = Table(title=f"Báo cáo Vòng phản hồi: {loop_type}")
    table.add_column("Hạng mục", style="cyan")
    table.add_column("Chi tiết kiểm duyệt", style="yellow")

    status_color = "green" if execution.status == "COMPLETED" else "red"
    table.add_row(
        "Trạng thái Vòng phản hồi",
        f"[bold {status_color}]{execution.status}[/bold {status_color}]",
    )
    table.add_row("Nhịp chu kỳ (Cadence)", execution.cadence)
    table.add_row("Logs gác cổng", "\n".join(execution.evidence_logs))

    console.print(table)

    if execution.status == "FAILED":
        raise typer.Exit(code=1)


# --- ĐỘNG CƠ QUẢN LÝ VÒNG ĐỜI TÀI LIỆU TỰ TRỊ (PHASE 4 - SPRINT DLM) ---


@app.command()
def dlm(
    path: str = typer.Argument(..., help="Đường dẫn tới tệp tin tài liệu"),
    status: str = typer.Argument(..., help="Trạng thái: DRAFT / ACTIVE / SUSPENDED"),
    reason: str = typer.Option(None, help="Lý do đình bản hoặc chuyển đổi"),
) -> None:
    """Quản lý vòng đời tài liệu tự trị có sao lưu mật mã vĩnh cửu."""
    console.print("[bold blue]Khởi chạy EAOS Document Lifecycle Controller...[/bold blue]\n")

    from pathlib import Path

    from engine.compiler.document_lifecycle_controller import (
        DocumentLifecycleController,
    )

    root_dir = Path(__file__).resolve().parent.parent.parent
    target_path = Path(path)

    if not target_path.exists():
        # Thử tìm kiếm tương đối từ thư mục docs/
        target_path = root_dir / "docs" / path

    if not target_path.exists():
        console.print(f"[bold red]Lỗi: Không tìm thấy tệp {path}[/bold red]")
        raise typer.Exit(code=1)

    controller = DocumentLifecycleController(root_dir)
    success = controller.transition_state(doc_path=target_path, target_status=status, reason=reason)

    if success:
        console.print(f"[bold green]✔ CHUYỂN TRẠNG THÁI VÒNG ĐỜI THÀNH CÔNG: {status.upper()}[/bold green]")
        console.print("  • Bản sao lưu lịch sử: [cyan]generated/docs/archive/[/cyan]")
    else:
        console.print("[bold red]✘ THẤT BẠI KHI CẬP NHẬT VÒNG ĐỜI.[/bold red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
