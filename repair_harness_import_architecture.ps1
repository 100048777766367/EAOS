#requires -Version 7.0
[CmdletBinding()]
param(
    [string]$Root = (Get-Location).Path,
    [switch]$NoTests
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Read-Utf8NoBom {
    param([Parameter(Mandatory)][string]$Path)

    $bytes = [System.IO.File]::ReadAllBytes($Path)
    if ($bytes.Length -ge 3 -and
        $bytes[0] -eq 0xEF -and
        $bytes[1] -eq 0xBB -and
        $bytes[2] -eq 0xBF) {
        throw "UTF-8 BOM detected before repair: $Path"
    }

    return [System.IO.File]::ReadAllText(
        $Path,
        [System.Text.UTF8Encoding]::new($false)
    )
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Content
    )

    [System.IO.File]::WriteAllText(
        $Path,
        $Content,
        [System.Text.UTF8Encoding]::new($false)
    )
}

function Assert-Utf8NoBom {
    param([Parameter(Mandatory)][string]$Path)

    $bytes = [System.IO.File]::ReadAllBytes($Path)
    if ($bytes.Length -ge 3 -and
        $bytes[0] -eq 0xEF -and
        $bytes[1] -eq 0xBB -and
        $bytes[2] -eq 0xBF) {
        throw "UTF-8 BOM detected: $Path"
    }
}

function Get-PythonFiles {
    param([Parameter(Mandatory)][string]$SearchRoot)

    $excluded = @(
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".eaos-repair-backup"
    )

    Get-ChildItem -LiteralPath $SearchRoot -Recurse -File -Filter "*.py" |
        Where-Object {
            $full = $_.FullName
            $skip = $false

            foreach ($name in $excluded) {
                $marker = [string]::Concat(
                    [IO.Path]::DirectorySeparatorChar,
                    $name,
                    [IO.Path]::DirectorySeparatorChar
                )

                if ($full.Contains($marker)) {
                    $skip = $true
                    break
                }
            }

            -not $skip
        }
}

function Backup-File {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Root,
        [Parameter(Mandatory)][string]$BackupRoot
    )

    $relative = [IO.Path]::GetRelativePath($Root, $Path)
    $destination = Join-Path $BackupRoot $relative
    $destinationDir = Split-Path -Parent $destination

    New-Item -ItemType Directory -Force -Path $destinationDir | Out-Null
    Copy-Item -LiteralPath $Path -Destination $destination -Force

    return $destination
}

$Root = (Resolve-Path -LiteralPath $Root).Path
$Packages = Join-Path $Root "packages"
$Harness = Join-Path $Packages "harness"
$EnterpriseHarness = Join-Path $Harness "enterprise_harness.py"
$PackageEngine = Join-Path $Harness "package_engine.py"
$PackageInit = Join-Path $Harness "__init__.py"

Write-Host ""
Write-Host "EAOS HARNESS IMPORT ARCHITECTURE REPAIR" -ForegroundColor Cyan
Write-Host "ROOT = $Root"
Write-Host ""

Write-Host "[1/8] Repository identity check" -ForegroundColor Yellow

if (-not (Test-Path -LiteralPath (Join-Path $Root ".git"))) {
    throw "Not an EAOS repository root: $Root"
}

foreach ($path in @($Packages, $Harness, $EnterpriseHarness, $PackageEngine, $PackageInit)) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Required EAOS path is missing: $path"
    }
}

Write-Host "Git repository = OK"
Write-Host "packages/ = OK"
Write-Host "packages/harness = OK"

Write-Host "[2/8] Canonical architecture check" -ForegroundColor Yellow

$enterpriseContent = Read-Utf8NoBom $EnterpriseHarness
$engineContent = Read-Utf8NoBom $PackageEngine
$initContent = Read-Utf8NoBom $PackageInit

if ($enterpriseContent -notmatch '\bclass\s+EAOSAgentHarnessControlPlane\b') {
    throw "Canonical EAOSAgentHarnessControlPlane not found in enterprise_harness.py"
}

if ($engineContent -notmatch '\bclass\s+EAOSEnterpriseHarnessPackageEngine\b') {
    throw "Canonical EAOSEnterpriseHarnessPackageEngine not found in package_engine.py"
}

if ($enterpriseContent -match '\bEAOSEnterpriseHarnessPackageEngine\b') {
    throw @"
Architecture inconsistency detected:
enterprise_harness.py contains EAOSEnterpriseHarnessPackageEngine.

This repair refuses to modify enterprise_harness.py automatically.
Review that file manually before continuing.
"@
}

Write-Host "ControlPlane owner = enterprise_harness.py"
Write-Host "PackageEngine owner = package_engine.py"
Write-Host "Canonical ownership = OK"

Write-Host "[3/8] Search repository for stale PackageEngine imports" -ForegroundColor Yellow

$pythonFiles = @(Get-PythonFiles -SearchRoot $Root)
$stale = @()

foreach ($file in $pythonFiles) {
    $content = Read-Utf8NoBom $file.FullName

    if ($content -match 'from\s+packages\.harness\.enterprise_harness\s+import[\s\S]{0,1000}?EAOSEnterpriseHarnessPackageEngine') {
        $stale += $file
    }
}

Write-Host "Python files scanned = $($pythonFiles.Count)"
Write-Host "Stale PackageEngine import sites = $($stale.Count)"

Write-Host "[4/8] Create repair backup" -ForegroundColor Yellow

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupRoot = Join-Path $Root ".eaos-repair-backup\harness-import-architecture\$timestamp"
New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null

Write-Host "Backup = $backupRoot"

Write-Host "[5/8] Repair only stale test/application imports" -ForegroundColor Yellow

$changed = [System.Collections.Generic.List[string]]::new()

foreach ($file in $stale) {
    $path = $file.FullName
    $content = Read-Utf8NoBom $path

    $newContent = $content

    # Case 1:
    # from packages.harness.enterprise_harness import (
    #     EAOSAgentHarnessControlPlane,
    #     EAOSEnterpriseHarnessPackageEngine,
    # )
    $patternCombined = '(?ms)^from\s+packages\.harness\.enterprise_harness\s+import\s*\(\s*EAOSAgentHarnessControlPlane\s*,\s*EAOSEnterpriseHarnessPackageEngine\s*,?\s*\)'

    if ($newContent -match $patternCombined) {
        $replacement = @'
from packages.harness import (
    EAOSAgentHarnessControlPlane,
    EAOSEnterpriseHarnessPackageEngine,
)
'@
        $newContent = [regex]::Replace(
            $newContent,
            $patternCombined,
            $replacement,
            1
        )
    }

    # Case 2:
    # from packages.harness.enterprise_harness import (
    #     EAOSEnterpriseHarnessPackageEngine,
    # )
    $patternEngineOnly = '(?ms)^from\s+packages\.harness\.enterprise_harness\s+import\s*\(\s*EAOSEnterpriseHarnessPackageEngine\s*,?\s*\)'

    if ($newContent -match $patternEngineOnly) {
        $replacement = @'
from packages.harness.package_engine import (
    EAOSEnterpriseHarnessPackageEngine,
)
'@
        $newContent = [regex]::Replace(
            $newContent,
            $patternEngineOnly,
            $replacement,
            1
        )
    }

    # Case 3:
    # from packages.harness.enterprise_harness import (
    #     EAOSEnterpriseHarnessPackageEngine,
    #     ...
    # )
    # This is intentionally rejected because automatically rearranging
    # arbitrary import lists can change formatting or semantics.
    if ($newContent -match 'from\s+packages\.harness\.enterprise_harness\s+import[\s\S]{0,1000}?EAOSEnterpriseHarnessPackageEngine') {
        throw @"
Unsupported stale import shape:
$path

The file imports PackageEngine from enterprise_harness.py, but its import
layout is not one of the safe canonical forms. No change was made to it.
Review it manually.
"@
    }

    if ($newContent -eq $content) {
        throw "Stale import was detected but no safe transformation matched: $path"
    }

    $null = Backup-File -Path $path -Root $Root -BackupRoot $backupRoot
    Write-Utf8NoBom -Path $path -Content $newContent
    $changed.Add($path)
    Write-Host "REPAIRED $path"
}

Write-Host "Files repaired = $($changed.Count)"

Write-Host "[6/8] Validate UTF-8 NO BOM and architecture consistency" -ForegroundColor Yellow

$validationFiles = @(
    $EnterpriseHarness,
    $PackageEngine,
    $PackageInit
) + $changed

foreach ($path in ($validationFiles | Select-Object -Unique)) {
    Assert-Utf8NoBom $path
}

foreach ($file in $pythonFiles) {
    $content = Read-Utf8NoBom $file.FullName

    if ($content -match 'from\s+packages\.harness\.enterprise_harness\s+import[\s\S]{0,1000}?EAOSEnterpriseHarnessPackageEngine') {
        throw "Stale PackageEngine import remains: $($file.FullName)"
    }
}

Write-Host "UTF-8 NO BOM = OK"
Write-Host "No stale enterprise_harness PackageEngine imports = OK"

Write-Host "[7/8] Validate public package API" -ForegroundColor Yellow

Push-Location $Root
try {
    $probe = @'
from packages.harness import (
    EAOSAgentHarnessControlPlane,
    EAOSEnterpriseHarnessPackageEngine,
)
from packages.harness.enterprise_harness import (
    EAOSAgentHarnessControlPlane as ControlPlane,
)
from packages.harness.package_engine import (
    EAOSEnterpriseHarnessPackageEngine as PackageEngine,
)

assert EAOSAgentHarnessControlPlane is ControlPlane
assert EAOSEnterpriseHarnessPackageEngine is PackageEngine

print("PUBLIC_API = OK")
print("CONTROL_PLANE_OWNER = OK")
print("PACKAGE_ENGINE_OWNER = OK")
'@

    $probePath = Join-Path $env:TEMP "eaos_harness_import_probe_$([Guid]::NewGuid().ToString('N')).py"

    try {
        Write-Utf8NoBom -Path $probePath -Content $probe
        & uv run python $probePath

        if ($LASTEXITCODE -ne 0) {
            throw "uv run python import probe failed with exit code $LASTEXITCODE"
        }
    }
    finally {
        Remove-Item -LiteralPath $probePath -Force -ErrorAction SilentlyContinue
    }
}
finally {
    Pop-Location
}

if (-not $NoTests) {
    Write-Host "[8/8] Run harness package test" -ForegroundColor Yellow

    Push-Location $Root
    try {
        & uv run pytest tests/unit/packages/test_harness_package.py -q

        if ($LASTEXITCODE -ne 0) {
            throw "Harness package test failed with exit code $LASTEXITCODE"
        }
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Host "[8/8] Pytest = SKIPPED (-NoTests)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==============================================" -ForegroundColor Green
Write-Host "HARNESS IMPORT ARCHITECTURE REPAIR = SUCCESS" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Write-Host ""
Write-Host "ControlPlane : packages/harness/enterprise_harness.py"
Write-Host "PackageEngine: packages/harness/package_engine.py"
Write-Host "Public API   : packages/harness/__init__.py"
Write-Host "Changed files: $($changed.Count)"
Write-Host "Backup       : $backupRoot"
Write-Host ""