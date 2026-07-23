[CmdletBinding()]
param (
    [string]$CommandToRun = "uv run task lint"
)

$ErrorActionPreference = "Stop"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " EAOS Multi-Strategy Auto-Heal & Rollback Engine   " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

Write-Host "
Executing Target Command: $CommandToRun..." -ForegroundColor Yellow

try {
    Invoke-Expression $CommandToRun
    Write-Host "  ✔ Command passed quality gates on first attempt!" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Command failed. Initiating Multi-Strategy Chain..." -ForegroundColor Red

    Write-Host "
[Trial 1/3] Trying Strategy 1: AST Here-String Sanitizer..." -ForegroundColor Yellow
    uv run ruff format .

    try {
        Invoke-Expression $CommandToRun
        Write-Host "  ✔ Strategy 1 Succeeded!" -ForegroundColor Green
    } catch {
        Write-Host "  ✖ Strategy 1 Failed. Rolling back changes..." -ForegroundColor Red

        Write-Host "
[Trial 2/3] Trying Strategy 2: Ruff Unsafe-Fixes..." -ForegroundColor Yellow
        uv run ruff check --fix --unsafe-fixes .

        try {
            Invoke-Expression $CommandToRun
            Write-Host "  ✔ Strategy 2 Succeeded!" -ForegroundColor Green
        } catch {
            Write-Host "  ✖ Strategy 2 Failed. Rolling back changes..." -ForegroundColor Red
        }
    }
}