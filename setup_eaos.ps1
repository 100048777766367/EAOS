Set-Location "D:\EAOS"

# Các file gốc
$rootFiles = @(
    "ARCHITECTURE_CONSTITUTION.md",
    "EAOS_CONSTITUTION.md",
    "GOVERNANCE.md",
    "SECURITY_POLICY.md",
    "ENGINEERING_GUIDE.md",
    "Tasks.md"
)
foreach ($f in $rootFiles) {
    if (-not (Test-Path ".\$f")) { New-Item -Name $f -ItemType File | Out-Null }
}

# Constitution
$constitutionFiles = @("system.constitution.md","architecture.constitution.md","execution.constitution.md","chat.constitution.md")
foreach ($f in $constitutionFiles) {
    if (-not (Test-Path ".\.eaos\constitution\$f")) { New-Item ".\.eaos\constitution\$f" -ItemType File | Out-Null }
}

# Governance
$governanceFiles = @("authority.yaml","blast-radius.yaml","mutation-policy.yaml","approval-policy.yaml","escalation-policy.yaml")
foreach ($f in $governanceFiles) {
    if (-not (Test-Path ".\.eaos\governance\$f")) { New-Item ".\.eaos\governance\$f" -ItemType File | Out-Null }
}

# Tasks
$taskFiles = @("task-registry.yaml","task-dependencies.yaml","task-contracts.yaml","task-state.json","task-history.jsonl")
foreach ($f in $taskFiles) {
    if (-not (Test-Path ".\.eaos\tasks\$f")) { New-Item ".\.eaos\tasks\$f" -ItemType File | Out-Null }
}

# Failures
$failureFiles = @("failure-registry.json","failure-schema.json","failure-lineage.json","causal-graph.json","failure-history.jsonl")
foreach ($f in $failureFiles) {
    if (-not (Test-Path ".\.eaos\failures\$f")) { New-Item ".\.eaos\failures\$f" -ItemType File | Out-Null }
}

# Recovery
$recoveryFiles = @("recovery-policy.yaml","recovery-state.json","rollback-manifest.json","checkpoint-registry.json","recovery-history.jsonl")
foreach ($f in $recoveryFiles) {
    if (-not (Test-Path ".\.eaos\recovery\$f")) { New-Item ".\.eaos\recovery\$f" -ItemType File | Out-Null }
}

# Evidence
$evidenceFiles = @("evidence-registry.json","evidence-schema.json","verification-runs.jsonl","command-results.jsonl","test-results.jsonl","runtime-observations.jsonl")
foreach ($f in $evidenceFiles) {
    if (-not (Test-Path ".\.eaos\evidence\$f")) { New-Item ".\.eaos\evidence\$f" -ItemType File | Out-Null }
}

# Contracts
$contractFiles = @("repository-contract.yaml","architecture-contract.yaml","api-contract.yaml","websocket-contract.yaml","runtime-contract.yaml","chat-contract.yaml","task-contract.yaml")
foreach ($f in $contractFiles) {
    if (-not (Test-Path ".\.eaos\contracts\$f")) { New-Item ".\.eaos\contracts\$f" -ItemType File | Out-Null }
}

# Schemas
$schemaFiles = @("task.schema.json","failure.schema.json","evidence.schema.json","checkpoint.schema.json","decision.schema.json","approval.schema.json","event.schema.json")
foreach ($f in $schemaFiles) {
    if (-not (Test-Path ".\.eaos\schemas\$f")) { New-Item ".\.eaos\schemas\$f" -ItemType File | Out-Null }
}

# Decisions
if (-not (Test-Path ".\.eaos\decisions\adr-registry.json")) { New-Item ".\.eaos\decisions\adr-registry.json" -ItemType File | Out-Null }
foreach ($sub in @("approved","proposed","superseded","rejected")) {
    if (-not (Test-Path ".\.eaos\decisions\$sub")) { New-Item ".\.eaos\decisions\$sub" -ItemType Directory | Out-Null }
}

# Runtime
$runtimeFiles = @("runtime-state.json","service-registry.json","process-registry.json","endpoint-registry.json","health-snapshot.json")
foreach ($f in $runtimeFiles) {
    if (-not (Test-Path ".\.eaos\runtime\$f")) { New-Item ".\.eaos\runtime\$f" -ItemType File | Out-Null }
}

# Events
if (-not (Test-Path ".\.eaos\events\event-ledger.jsonl")) { New-Item ".\.eaos\events\event-ledger.jsonl" -ItemType File | Out-Null }

# Checkpoints
if (-not (Test-Path ".\.eaos\checkpoints\checkpoint-registry.json")) { New-Item ".\.eaos\checkpoints\checkpoint-registry.json" -ItemType File | Out-Null }
foreach ($sub in @("manifests","hashes")) {
    if (-not (Test-Path ".\.eaos\checkpoints\$sub")) { New-Item ".\.eaos\checkpoints\$sub" -ItemType Directory | Out-Null }
}

# Scenarios
$scenarioFiles = @("scenarios.yaml","failure-scenarios.yaml","recovery-scenarios.yaml","what-if-scenarios.yaml")
foreach ($f in $scenarioFiles) {
    if (-not (Test-Path ".\.eaos\scenarios\$f")) { New-Item ".\.eaos\scenarios\$f" -ItemType File | Out-Null }
}

# Policies (có nội dung mẫu)
$policyFiles = @("invariants.yaml","forbidden-mutations.yaml","protected-paths.yaml","protected-contracts.yaml","safety-gates.yaml")
foreach ($f in $policyFiles) {
    $path = ".\.eaos\policies\$f"
    if (-not (Test-Path $path)) {
        New-Item $path -ItemType File | Out-Null
        if ($f -eq "protected-paths.yaml") {
            @"
protected_paths:
  - .git/**
  - .venv/**
  - eaos_backups/**
"@ | Out-File $path
        }
        elseif ($f -eq "forbidden-mutations.yaml") {
            @"
forbidden:
  - modify_constitution_without_approval
  - delete_evidence
  - overwrite_checkpoint
"@ | Out-File $path
        }
    }
}

# Manifests (có nội dung mẫu)
$manifestFiles = @("system-manifest.json","capability-manifest.json","skill-manifest.json","contract-manifest.json","version-manifest.json")
foreach ($f in $manifestFiles) {
    $path = ".\.eaos\manifests\$f"
    if (-not (Test-Path $path)) {
        New-Item $path -ItemType File | Out-Null
        if ($f -eq "system-manifest.json") {
            @"
{
  "EAOS": {
    "Constitution": "v3",
    "Governance": "v2",
    "Tasks": "1–20",
    "Skills": 8,
    "Contracts": 17,
    "Policies": 12,
    "Schemas": 9,
    "Evidence Engine": "v1"
  }
}
"@ | Out-File $path
        }
    }
}

# .agents\skills
if (-not (Test-Path ".\.agents\skills")) { New-Item ".\.agents\skills" -ItemType Directory | Out-Null }

# source code
if (-not (Test-Path ".\source code")) { New-Item ".\source code" -ItemType Directory | Out-Null }
