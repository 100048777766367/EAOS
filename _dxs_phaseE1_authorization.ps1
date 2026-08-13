$ErrorActionPreference = "Stop"

Write-Host "============================================================"
Write-Host " PHASE E.1 AUTHORIZATION GATE"
Write-Host "============================================================"

$checks = @()

function Add-Check {
    param(
        [string]$Name,
        [bool]$Passed,
        [string]$Detail
    )

    $script:checks += [PSCustomObject]@{
        Name = $Name
        Passed = $Passed
        Detail = $Detail
    }

    if ($Passed) {
        Write-Host "[PASS] $Name"
    }
    else {
        Write-Host "[FAIL] $Name"
    }
}


Add-Check `
"Exact Phase E objective" `
(-not [string]::IsNullOrWhiteSpace($env:DXS_PHASE_E_OBJECTIVE)) `
$env:DXS_PHASE_E_OBJECTIVE


Add-Check `
"Acceptance criteria" `
(-not [string]::IsNullOrWhiteSpace($env:DXS_PHASE_E_ACCEPTANCE)) `
$env:DXS_PHASE_E_ACCEPTANCE


Add-Check `
"Relevant specification" `
(-not [string]::IsNullOrWhiteSpace($env:DXS_PHASE_E_SPEC)) `
$env:DXS_PHASE_E_SPEC


Add-Check `
"Relevant contracts/interfaces" `
(-not [string]::IsNullOrWhiteSpace($env:DXS_PHASE_E_CONTRACTS)) `
$env:DXS_PHASE_E_CONTRACTS


Add-Check `
"Implementation surface" `
(-not [string]::IsNullOrWhiteSpace($env:DXS_PHASE_E_IMPLEMENTATION)) `
$env:DXS_PHASE_E_IMPLEMENTATION


Add-Check `
"Focused test surface" `
(-not [string]::IsNullOrWhiteSpace($env:DXS_PHASE_E_TESTS)) `
$env:DXS_PHASE_E_TESTS


Add-Check `
"Required validation commands" `
(-not [string]::IsNullOrWhiteSpace($env:DXS_PHASE_E_VALIDATION)) `
$env:DXS_PHASE_E_VALIDATION


$failed = @($checks | Where-Object { -not $_.Passed })


Write-Host ""
Write-Host "============================================================"

if ($failed.Count -gt 0) {

    Write-Host " PHASE E.1 STATUS: UNAUTHORIZED"

    foreach ($item in $failed) {
        Write-Host "[ ] $($item.Name)"
    }

    exit 2
}


Write-Host " PHASE E.1 STATUS: AUTHORIZED"
Write-Host "============================================================"