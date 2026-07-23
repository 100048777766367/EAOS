[CmdletBinding()]
param (
    [string]$Action = "status"
)

$ErrorActionPreference = "Stop"
$utf8NoBom = New-Object System.Text.UTF8Encoding($False)

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " EAOS Master System Operational Control Unit        " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

switch ($Action.ToLower()) {
    "bootstrap" {
        Write-Host "`n[1/4] Starting Docker Storage Stack..." -ForegroundColor Yellow
        docker compose -f infra/compose/docker-compose.prod.yml up -d --remove-orphans

        Write-Host "`n[2/4] Running AST Boundary Validator..." -ForegroundColor Yellow
        uv run task validate

        Write-Host "`n[3/4] Running Master Test Suite..." -ForegroundColor Yellow
        uv run task test

        Write-Host "`n[4/4] Recording Production Release Snapshot..." -ForegroundColor Yellow
        uv run task time_machine record "EAOS_PROD_SUPREME_RELEASE_V1.0"
        Write-Host "`n✔ System Bootstrapped Successfully." -ForegroundColor Green
    }
    "audit" {
        Write-Host "`n[1/2] Computing Architectural Metrics..." -ForegroundColor Yellow
        uv run task metrics

        Write-Host "`n[2/2] Executing 3 Cybernetic Loops..." -ForegroundColor Yellow
        uv run task loop EXECUTION
        uv run task loop ARCHITECTURE
        uv run task task loop STRATEGY
        Write-Host "`n✔ Audit Complete." -ForegroundColor Green
    }
    "status" {
        Write-Host "`nChecking Monorepo Quality Gates..." -ForegroundColor Yellow
        uv run task lint
        uv run task validate
        uv run task metrics
    }
    default {
        Write-Host "Usage: .\scripts\eaos_master_control.ps1 -Action [bootstrap | audit | status]" -ForegroundColor Yellow
    }
}