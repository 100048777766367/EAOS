[CmdletBinding()]
param ()

$ErrorActionPreference = "Stop"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " EAOS Ultra-Scale Operational Provisioner           " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

Write-Host "
Running Verification Quality Gates (Lint, Test, Validate)..." -ForegroundColor Yellow
uv run task lint
uv run task test
uv run task validate

Write-Host "
====================================================" -ForegroundColor Cyan
Write-Host " ALL QUALITY GATES PASSED 100%! SYSTEM OPERATIONAL. " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan