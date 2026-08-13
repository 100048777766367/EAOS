$ErrorActionPreference = "Stop"

$Root = "D:\EAOS"
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$EvidenceDir = Join-Path $Root "artifacts\validation"
$Evidence = Join-Path $EvidenceDir "dxs_phaseE0_spec_discovery_$Stamp.txt"

New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null

$Out = [System.Collections.Generic.List[string]]::new()

function Add-Out([string]$Text = "") {
    [void]$Out.Add($Text)
    Write-Host $Text
}

function Section([string]$Title) {
    Add-Out ""
    Add-Out "============================================================"
    Add-Out $Title
    Add-Out "============================================================"
}

Add-Out "DXS PHASE E.0 — SPECIFICATION / CONTRACT DISCOVERY"
Add-Out "Timestamp: $Stamp"
Add-Out "Repository: $Root"
Add-Out "Baseline: D.1-R4"

Section "1. REPOSITORY SPECIFICATION SURFACE"

$SpecRoots = @(
    "specifications",
    "docs",
    "architecture",
    "adr",
    "ADRs",
    ".github"
)

foreach ($Rel in $SpecRoots) {
    $Path = Join-Path $Root $Rel

    if (Test-Path $Path) {
        Add-Out "[FOUND] $Path"

        Get-ChildItem `
            -Path $Path `
            -Recurse `
            -File `
            -Include *.md,*.txt,*.yaml,*.yml,*.json `
            -ErrorAction SilentlyContinue |
            Sort-Object FullName |
            ForEach-Object {
                Add-Out "  $($_.FullName)"
            }
    }
    else {
        Add-Out "[MISS]  $Path"
    }
}

Section "2. SPECIFICATION FILE HEADERS"

$SpecFiles = Get-ChildItem `
    -Path $Root `
    -Recurse `
    -File `
    -Include *.md,*.txt `
    -ErrorAction SilentlyContinue |
    Where-Object {
        $_.FullName -notmatch "\\\.venv\\" -and
        $_.FullName -notmatch "\\__pycache__\\" -and
        $_.FullName -notmatch "\\artifacts\\" -and
        $_.FullName -notmatch "\\.git\\"
    } |
    Where-Object {
        $_.FullName -match "\\specifications\\" -or
        $_.Name -match "spec|contract|architecture|adr|phase"
    } |
    Sort-Object FullName

foreach ($File in $SpecFiles) {
    Add-Out ""
    Add-Out "--- $($File.FullName) ---"

    Get-Content `
        -Path $File.FullName `
        -TotalCount 40 `
        -ErrorAction SilentlyContinue |
        ForEach-Object {
            Add-Out "  $_"
        }
}

Section "3. SEARCH FOR PHASE / CONTRACT LANGUAGE"

$SearchPatterns = @(
    "Phase E",
    "PHASE E",
    "E.0",
    "E.1",
    "Phase E objective",
    "acceptance criteria",
    "acceptance",
    "contract",
    "capability",
    "knowledge",
    "compiler",
    "repository",
    "representation",
    "storage",
    "ontology",
    "lifecycle",
    "view"
)

$SearchFiles = Get-ChildItem `
    -Path $Root `
    -Recurse `
    -File `
    -Include *.py,*.md,*.txt,*.yaml,*.yml,*.json `
    -ErrorAction SilentlyContinue |
    Where-Object {
        $_.FullName -notmatch "\\\.venv\\" -and
        $_.FullName -notmatch "\\__pycache__\\" -and
        $_.FullName -notmatch "\\artifacts\\" -and
        $_.FullName -notmatch "\\.git\\"
    }

foreach ($Pattern in $SearchPatterns) {
    Add-Out ""
    Add-Out "--- SEARCH: $Pattern ---"

    $Matches = $SearchFiles |
        Select-String `
            -Pattern $Pattern `
            -SimpleMatch `
            -ErrorAction SilentlyContinue |
        Select-Object -First 80

    if ($Matches) {
        foreach ($Match in $Matches) {
            Add-Out "$($Match.Path):$($Match.LineNumber): $($Match.Line.Trim())"
        }
    }
    else {
        Add-Out "[NONE]"
    }
}

Section "4. DXS CONTRACT / INTERFACE SURFACE"

$ContractRoot = Join-Path $Root "dxs\contracts"

if (Test-Path $ContractRoot) {
    Get-ChildItem `
        -Path $ContractRoot `
        -Recurse `
        -File `
        -Filter "*.py" |
        Sort-Object FullName |
        ForEach-Object {
            Add-Out "[CONTRACT] $($_.FullName)"
        }
}
else {
    Add-Out "[MISS] $ContractRoot"
}

Section "5. DXS APPLICATION / DOMAIN SURFACE"

$SurfaceRoots = @(
    "dxs\application",
    "dxs\domain",
    "dxs\ports",
    "dxs\adapters",
    "dxs\scaffolding",
    "dxs\evolution",
    "dxs\ai",
    "dxs\migration",
    "dxs\validation"
)

foreach ($Rel in $SurfaceRoots) {
    $Path = Join-Path $Root $Rel

    if (Test-Path $Path) {
        Add-Out ""
        Add-Out "--- $Path ---"

        Get-ChildItem `
            -Path $Path `
            -Recurse `
            -File `
            -Filter "*.py" |
            Sort-Object FullName |
            ForEach-Object {
                Add-Out "  $($_.FullName)"
            }
    }
}

Section "6. TEST SURFACE"

$TestRoots = @(
    "tests",
    "dxs\tests"
)

foreach ($Rel in $TestRoots) {
    $Path = Join-Path $Root $Rel

    if (Test-Path $Path) {
        Add-Out ""
        Add-Out "--- TEST ROOT: $Path ---"

        Get-ChildItem `
            -Path $Path `
            -Recurse `
            -File `
            -Include *.py `
            -ErrorAction SilentlyContinue |
            Sort-Object FullName |
            ForEach-Object {
                Add-Out "  $($_.FullName)"
            }
    }
}

Section "7. GIT HISTORY — PHASE / SPECIFICATION CLUES"

if (Get-Command git -ErrorAction SilentlyContinue) {

    Add-Out "--- Recent commits ---"

    git log --oneline --decorate -40 2>&1 |
        ForEach-Object {
            Add-Out $_
        }

    Add-Out ""
    Add-Out "--- Commit search: Phase E ---"

    git log --all --oneline --decorate `
        --grep="Phase E" `
        --regexp-ignore-case 2>&1 |
        ForEach-Object {
            Add-Out $_
        }

    Add-Out ""
    Add-Out "--- Commit search: specification ---"

    git log --all --oneline --decorate `
        --grep="specification" `
        --regexp-ignore-case 2>&1 |
        ForEach-Object {
            Add-Out $_
        }

    Add-Out ""
    Add-Out "--- Commit search: contract ---"

    git log --all --oneline --decorate `
        --grep="contract" `
        --regexp-ignore-case 2>&1 |
        ForEach-Object {
            Add-Out $_
        }

    Add-Out ""
    Add-Out "--- Relevant specification paths in history ---"

    git log --all --name-only --pretty=format: -- `
        specifications `
        docs `
        architecture `
        adr 2>&1 |
        Where-Object {
            $_ -and $_.Trim()
        } |
        Select-Object -Unique |
        Select-Object -First 300 |
        ForEach-Object {
            Add-Out $_
        }
}

Section "8. CURRENT GIT STATE"

if (Get-Command git -ErrorAction SilentlyContinue) {

    Add-Out "--- STATUS ---"

    git status --short 2>&1 |
        ForEach-Object {
            Add-Out $_
        }

    Add-Out ""
    Add-Out "--- BRANCH ---"

    git branch --show-current 2>&1 |
        ForEach-Object {
            Add-Out $_
        }

    Add-Out ""
    Add-Out "--- HEAD ---"

    git rev-parse HEAD 2>&1 |
        ForEach-Object {
            Add-Out $_
        }
}

Section "9. E.1 AUTHORIZATION GATE"

Add-Out "[STATUS] READ-ONLY DISCOVERY ONLY"
Add-Out ""
Add-Out "[PASS] No restore performed."
Add-Out "[PASS] No implementation modified."
Add-Out "[PASS] No tests modified."
Add-Out "[PASS] No patch performed."
Add-Out "[PASS] No focused tests run."
Add-Out "[PASS] No full pytest."
Add-Out "[PASS] No async."
Add-Out "[PASS] No E2E."
Add-Out ""
Add-Out "E.1 remains UNAUTHORIZED until:"
Add-Out "  [ ] Exact Phase E objective"
Add-Out "  [ ] Acceptance criteria"
Add-Out "  [ ] Relevant specification"
Add-Out "  [ ] Relevant contracts/interfaces"
Add-Out "  [ ] Implementation surface"
Add-Out "  [ ] Focused test surface"
Add-Out "  [ ] Required validation commands"

$OutText = $Out -join [Environment]::NewLine

Set-Content `
    -Path $Evidence `
    -Value $OutText `
    -Encoding UTF8

Write-Host ""
Write-Host "============================================================"
Write-Host " PHASE E.0 SPEC DISCOVERY COMPLETE"
Write-Host "============================================================"
Write-Host ""
Write-Host "[PASS] Read-only discovery."
Write-Host "[PASS] No restore."
Write-Host "[PASS] No patch."
Write-Host "[PASS] No implementation changes."
Write-Host "[PASS] No test changes."
Write-Host ""
Write-Host "[EVIDENCE] $Evidence"
