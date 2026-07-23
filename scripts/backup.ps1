# ==============================================================================
# EAOS SYSTEM BACKUP & LEDGER ARCHIVAL SCRIPT
# Workspace: D:\EAOS
# ==============================================================================

$ErrorActionPreference = "Stop"
$utf8NoBom = New-Object System.Text.UTF8Encoding($False)
$root = Get-Location

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " EAOS Audit Ledger Backup & System Archival         " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

$backupDir = Join-Path $root.Path "runtime\traces\backups"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ledgerFile = Join-Path $root.Path "runtime\traces\audit_ledger.jsonl"

if (Test-Path $ledgerFile) {
    $archiveName = "audit_ledger_$timestamp.jsonl"
    $destination = Join-Path $backupDir $archiveName
    Copy-Item -Path $ledgerFile -Destination $destination -Force
    Write-Host "`n[✔] Audit ledger successfully archived to:" -ForegroundColor Green
    Write-Host "    $destination" -ForegroundColor Gray
} else {
    Write-Host "`n[!] Ledger file not found at $ledgerFile. Creating placeholder..." -ForegroundColor Yellow
    [System.IO.File]::WriteAllText($ledgerFile, "", $utf8NoBom)
    Write-Host "    Created placeholder at $ledgerFile" -ForegroundColor Gray
}

Write-Host "`n====================================================" -ForegroundColor Cyan
Write-Host " BACKUP COMPLETED SUCCESSFULLY                      " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan