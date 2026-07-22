# ==============================================================================
# EAOS AUTONOMOUS MASTER RUNBOOK & QUALITY GATE (POWERSHELL AUTOMATION)
# ==============================================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   EAOS OPERATING SYSTEM - AUTONOMOUS MASTER RUNBOOK     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Dọn sạch ký tự ẩn UTF-8 BOM toàn bộ repository
Write-Host "
[1/6] Dọn sạch ký tự ẩn UTF-8 BOM trên toàn bộ mã nguồn..." -ForegroundColor Yellow
uv run python -c "from pathlib import Path; [p.write_text(p.read_text(encoding='utf-8-sig'), encoding='utf-8') for p in Path('.').rglob('*.py') if p.is_file() and '.venv' not in p.parts]"
Write-Host "✔ Đã dọn sạch UTF-8 BOM." -ForegroundColor Green

# 2. Khởi chạy Ruff Linter & MyPy Type Checker
Write-Host "
[2/6] Chạy gác cổng Linter & Type-Checking..." -ForegroundColor Yellow
uv run task lint
if ($LASTEXITCODE -ne 0) {
    Write-Host "✘ LỖI LINTER/TYPING: Dừng tiến trình!" -ForegroundColor Red
    exit 1
}

# 3. Khởi chạy 39 Bài Test Tích Hợp Master
Write-Host "
[3/6] Chạy toàn bộ 39 bài Test Tích Hợp Master..." -ForegroundColor Yellow
uv run task test
if ($LASTEXITCODE -ne 0) {
    Write-Host "✘ LỖI TESTING: Dừng tiến trình!" -ForegroundColor Red
    exit 1
}

# 4. Kiểm toán ranh giới kiến trúc AST (Architecture Validator)
Write-Host "
[4/6] Chạy gác cổng Hiến pháp Kiến trúc AST..." -ForegroundColor Yellow
uv run task validate
if ($LASTEXITCODE -ne 0) {
    Write-Host "✘ LỖI KIẾN TRÚC: Phát hiện vi phạm ranh giới!" -ForegroundColor Red
    exit 1
}

# 5. Tự động sinh Đồ thị Phụ thuộc & Tính toán Chỉ số Sức khỏe
Write-Host "
[5/6] Tự động sinh Đồ thị Phụ thuộc & Tính toán Metrics..." -ForegroundColor Yellow
uv run task graph
uv run task metrics

# 6. Khóa mốc Baseline sản xuất mới vào Cỗ máy thời gian (Time Machine)
Write-Host "
[6/6] Khóa Mốc Release Sản Xuất vào Cỗ Máy Thời Gian..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
uv run python -m apps.cli.main time-machine record "prod_release_$timestamp"

Write-Host "
==========================================================" -ForegroundColor Green
Write-Host " ✔ EAOS KHẾP KÍN HOÀN HẢO! HỆ THỐNG ĐÃ SẴN SÀNG SẢN XUẤT. " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green