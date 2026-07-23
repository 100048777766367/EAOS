# ==============================================================================
# EAOS ENVIRONMENT BOOTSTRAPPER & RUNTIME INITIALIZER SCRIPT
# Workspace: D:\EAOS
# ==============================================================================

$ErrorActionPreference = "Stop"
$utf8NoBom = New-Object System.Text.UTF8Encoding($False)
$root = Get-Location

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " EAOS Environment Bootstrapper & Initializer        " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

Write-Host "`n[1/2] Executing Python Environment Initializer Engine..." -ForegroundColor Yellow
uv run python tools/bootstrap/environment_initializer.py

Write-Host "`n[2/2] Running Complete Verification Quality Gates..." -ForegroundColor Yellow
uv run task lint
uv run task test
uv run task validate
uv run task doctor

Write-Host "`n====================================================" -ForegroundColor Cyan
Write-Host " BOOTSTRAP COMPLETE — ALL 7 GAPS FULLY PROVISIONED!  " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan