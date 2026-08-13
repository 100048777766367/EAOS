#requires -Version 5.1
<#
.SYNOPSIS
    Install the 8 EAOS Antigravity skills directly into D:\EAOS\.agents\skills\

.DESCRIPTION
    Creates the exact EAOS skill tree requested by the repository workflow.
    Writes every SKILL.md as UTF-8 without BOM.
    Does not modify EAOS source code, .venv, Git metadata, or backup folders.

    Target:
        D:\EAOS\.agents\skills\

    Skills:
        eaos-architecture
        eaos-repository-engineering
        eaos-verification
        eaos-runtime-debugging
        eaos-api-websocket
        eaos-testing
        eaos-security
        eaos-safe-modification
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = 'D:\EAOS'
$SkillsRoot = Join-Path $RepoRoot '.agents\skills'

if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) {
    throw "EAOS repository root does not exist: $RepoRoot"
}

# Never touch protected repository content.
$Protected = @(
    (Join-Path $RepoRoot 'eaos_backups'),
    (Join-Path $RepoRoot '.venv'),
    (Join-Path $RepoRoot '.eaos_backups'),
    (Join-Path $RepoRoot '.eaos-repair-backup'),
    (Join-Path $RepoRoot '.git')
)

function Assert-NotProtected {
    param([Parameter(Mandatory)][string]$Path)

    $full = [IO.Path]::GetFullPath($Path).TrimEnd('\')
    foreach ($p in $Protected) {
        $protectedFull = [IO.Path]::GetFullPath($p).TrimEnd('\')
        if ($full.Equals($protectedFull, [StringComparison]::OrdinalIgnoreCase) -or
            $full.StartsWith($protectedFull + '\', [StringComparison]::OrdinalIgnoreCase)) {
            throw "Protected path operation blocked: $full"
        }
    }
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Content
    )

    Assert-NotProtected -Path $Path
    $encoding = New-Object System.Text.UTF8Encoding($false)
    [IO.File]::WriteAllText($Path, $Content, $encoding)
}

New-Item -ItemType Directory -Force -Path $SkillsRoot | Out-Null

$Skills = @{}

$Skills[@'
eaos-architecture
'@] = @'
---
name: eaos-architecture
description: EAOS architecture governance skill for Clean/Hexagonal Architecture, Ports and Adapters, dependency direction, package boundaries, Pydantic models, and ArchitectureValidator verification.
---

# EAOS Architecture Governance

## Mission

Preserve EAOS architectural integrity while allowing controlled evolution.

Use the actual repository architecture and validators as the source of truth.

## Principles

Prefer:
- Clean Architecture;
- Hexagonal Architecture;
- Ports and Adapters;
- dependency inversion;
- explicit boundaries;
- immutable value objects where appropriate;
- infrastructure behind adapters;
- thin interface layers;
- deterministic validation.

Avoid:
- domain importing web frameworks;
- business logic in CLI handlers;
- scattered direct database access;
- circular dependencies;
- hidden service locators;
- bypassing existing ports;
- duplicate abstractions.

## Source roots

Potential architectural areas:
`apps`, `packages`, `kernel`, `engine`, `tools`, `platforms`, `capabilities`, `governances`, `federations`, `observabilitys`, `securitys`, `agents`, `ai`, `runtime`, `schemas`, `sdk`, `validation`, `services`, `designs`, `locales`.

Inspect actual package metadata before assigning a layer.

## Dependency review

Before adding an import:
1. identify importing layer;
2. identify imported layer;
3. verify direction;
4. reuse existing protocol/port where possible;
5. avoid unnecessary abstractions;
6. run architecture validation after structural changes.

## Pydantic

Where Pydantic v2 is used:
- use v2 APIs;
- use `ConfigDict` according to repository conventions;
- use frozen models/value objects where immutability is part of the contract;
- keep domain invariants explicit;
- do not move domain rules into presentation-only validation.

## Typing

The project declares Python 3.14.

Prefer:
```python
list[str]
dict[str, int]
str | None
```

Avoid unnecessary `Any` and broad ignores.

## Architecture validation

Verify the complete path:
```text
ArchitectureValidator
→ validate_architecture()
→ ArchitectureValidationReport
→ passed/errors
→ CLI output
→ exit code
```

A successful-looking CLI output is insufficient if the process exits unsuccessfully.

## Structural change workflow

1. Map affected modules.
2. Identify contracts/interfaces.
3. Update implementation.
4. Update adapters.
5. Update tests.
6. Run lint/type checks.
7. Run architecture validation.
8. Run runtime checks if the change is executable.

## Anti-patterns

Look for:
- forbidden cross-layer imports;
- duplicate ports;
- adapters imported into domain code;
- circular imports;
- dead compatibility layers;
- hidden constructor side effects;
- fragile runtime imports;
- duplicated validation logic.

## Architecture report

Report:
- boundary changed;
- reason;
- old dependency direction;
- new dependency direction;
- contracts changed;
- tests;
- validator result;
- residual risks.

Never claim architecture compliance without running the repository validator when available.

'@

$Skills[@'
eaos-repository-engineering
'@] = @'
---
name: eaos-repository-engineering
description: End-to-end repository engineering and verification workflow for EAOS. Use for dependency synchronization, repository checks, formatting, linting, type checking, tests, Task/Make validation, architecture validation, service startup, runtime checks, and final evidence reports.
---

# EAOS Repository Engineering

## Objective

Execute a real repository verification pipeline for `D:\EAOS`.

The pipeline is evidence-driven. Do not infer success from configuration files or previous reports.

## Safety

Before mutation:
1. Confirm repository root.
2. Inspect Git status.
3. Confirm protected paths are not targeted.
4. Prefer repository-native commands.
5. Never use destructive cleanup as a verification prerequisite.

Protected:
- `D:\EAOS\eaos_backups\`
- `D:\EAOS\.venv\`
- `D:\EAOS\.eaos_backups\`
- `D:\EAOS\.eaos_contract_backup_*`
- `D:\EAOS\.eaos-repair-backup\`

## Pipeline

### 1. Discovery

Inspect existing paths such as:
`pyproject.toml`, `uv.lock`, `README.md`, Taskfile, Makefile, `apps/`, `packages/`, `kernel/`, `engine/`, `tools/`, `platforms/`, `capabilities/`, `governances/`, `federations/`, `observabilitys/`, `securitys/`, `agents/`, `ai/`, `runtime/`, `schemas/`, `sdk/`, `validation/`, `services/`, `designs/`, `locales/`, `tests/`, `fitness/`.

Only inspect paths that exist.

### 2. Dependency

Run:
```powershell
uv lock
uv sync
```

If `uv.lock` changes, inspect the diff. Do not overwrite backups.

### 3. Format

Use repository-native formatting commands first.

Possible:
```powershell
uv run ruff format .
```

If the project policy requires Python lines below 88 characters, verify that separately. Do not confuse Ruff''s configured `line-length` with the stricter repository policy.

### 4. Lint

Inspect the actual task definition before assuming scope.

Possible:
```powershell
uv run ruff check --fix .
uv run task lint
```

If the task does not cover every intended source root, run explicit checks for the missing roots and report the coverage gap.

### 5. Type check

Run the configured mypy command. Preserve strictness. Do not globally disable errors to obtain a green build.

### 6. Tests

Run the repository''s configured test command, for example:
```powershell
uv run task test
uv run pytest tests/
```

Include `fitness/` if it is part of the configured acceptance scope.

Record collection, pass, fail, skip, error, and exit code.

### 7. Taskfile/Makefile

If Taskfile or Makefile exists, inspect actual targets. Do not invent `doctor`, `lint`, `test`, or `run` targets.

Run only relevant existing targets.

### 8. Doctor and validation

Use actual repository commands, such as:
```powershell
uv run task doctor
uv run task validate
```

or their direct Python equivalents.

For architecture validation, verify:
```text
ArchitectureValidator
→ validate_architecture()
→ ArchitectureValidationReport
→ passed/errors
→ CLI output
→ exit status
```

### 9. Runtime

Start the actual API:
```powershell
uv run uvicorn apps.api.app.main:app --host 127.0.0.1 --port 8000 --reload
```

If a separate web app is required:
```powershell
uv run uvicorn apps.web.app.main:app --host 127.0.0.1 --port 3002 --reload
```

Verify the process actually listens.

### 10. Runtime endpoints

Check applicable:
`/health`, `/docs`, `/redoc`, `/metrics`, `/chat`.

Use the correct HTTP method/protocol. Do not use HEAD as a generic substitute.

For `/chat`, determine whether it is HTTP, WebSocket, streaming, or UI.

### 11. Docker

Only start Docker Compose when required/requested. Inspect the compose configuration first.

Safe default:
```powershell
docker compose up -d
```

Do not automatically use:
`docker compose down -v`, `docker system prune`, or `docker volume prune`.

## Root-cause loop

FAIL
→ exact command/status
→ first meaningful root cause
→ inspect source/config/dependency
→ targeted fix
→ targeted verification
→ affected verification
→ broader verification if required

Do not repeatedly rerun the same failed command without investigation.

## Evidence ledger

Track:
- stage;
- exact command;
- exit/status;
- evidence;
- result.

A missing result is UNVERIFIED.

## Completion

PASS only when every required stage has executable evidence.

BLOCKED when a required stage cannot be executed because of a real blocker.

PARTIAL when the requested scope intentionally excludes optional stages.

'@

$Skills[@'
eaos-verification
'@] = @'
---
name: eaos-verification
description: Master orchestration skill for the EAOS monorepo. Use when a task spans repository inspection, architecture, dependency synchronization, coding, linting, type checking, testing, validation, service startup, runtime debugging, WebSocket/API verification, or security-sensitive changes.
---

# EAOS Engineer — Master Orchestrator

## Mission

Act as the repository-level engineering orchestrator for `D:\EAOS`.

The objective is not merely to modify source code. The objective is to move EAOS from a known state to a **verified state**, using executable evidence.

A task is complete only when:
1. The requested change is implemented.
2. Architectural constraints are preserved.
3. Protected files/directories are untouched.
4. Relevant static checks pass.
5. Relevant tests pass.
6. Architecture validation passes when applicable.
7. Runtime behavior is verified when applicable.
8. Failures are explained by root cause, not hidden or bypassed.
9. The final report distinguishes verified facts from assumptions.

Never claim PASS because source code "looks correct".

## Mandatory operating model

Use this sequence unless the user explicitly requests a narrower operation:

DISCOVER
→ PROTECT
→ UNDERSTAND
→ PLAN
→ CHANGE
→ FORMAT
→ LINT
→ TYPE-CHECK
→ TEST
→ ARCHITECTURE-VALIDATE
→ BOOT
→ RUNTIME-VERIFY
→ SECURITY-CHECK
→ REPORT

For a runtime-only task, start at DISCOVER and execute only the applicable downstream stages.

## DISCOVER

Before changing code:
- Confirm the working directory is `D:\EAOS`.
- Inspect Git status.
- Inspect the repository root and relevant package directories.
- Read `pyproject.toml`, relevant Taskfile/Makefile files, entry points, and configuration.
- Locate the actual implementation before editing.
- Identify tests covering the affected behavior.
- Identify runtime services and ports involved.

Do not assume a path exists because a prompt names it.

## PROTECT

Treat these as protected unless explicitly authorized:
- `D:\EAOS\eaos_backups\`
- `D:\EAOS\.venv\`
- `D:\EAOS\.eaos_backups\`
- `D:\EAOS\.eaos_contract_backup_*`
- `D:\EAOS\.eaos-repair-backup\`
- `D:\EAOS\.git\`

Never delete, clean, overwrite, rename, move, or bulk-rewrite protected content.

## UNDERSTAND

Establish:
- current architecture;
- dependency/workspace structure;
- source of truth for configuration;
- command entry points;
- API/WebSocket routes;
- test boundaries;
- generated files;
- static assets;
- database/infrastructure dependencies.

For an existing bug, reproduce it before fixing it whenever practical.

## PLAN

For non-trivial work, identify:
- observed failure;
- likely root cause;
- evidence needed;
- files likely to change;
- validation commands;
- runtime checks;
- safety considerations.

Prefer the smallest structural fix that solves the actual root cause.

Never "fix" a failure by weakening tests, disabling validation, suppressing errors, or hiding failures.

## CHANGE

When modifying code:
- Preserve existing architecture.
- Prefer existing ports/interfaces/adapters.
- Keep business logic out of HTTP handlers when layers are separated.
- Keep infrastructure access behind adapters/ports.
- Preserve public APIs unless the task requires a change.
- Add/update tests for behavior changes.
- Keep JavaScript in static assets when that is the repository architecture.
- Keep Python source lines under 88 characters when editing code.
- Use Python 3.14-compatible typing.
- Use Pydantic v2 conventions.

## Verification

A check is VERIFIED only when the actual command succeeds.

Examples:
- Ruff: exit code 0.
- Mypy: exit code 0.
- Pytest: exit code 0 with expected tests executed.
- Architecture validation: underlying validator and CLI both succeed.
- HTTP: actual request returns expected result.
- WebSocket: actual handshake and message exchange succeed.
- Startup: service is actually listening and healthy.

"Command was started" is not "command passed".

## Failure loop

FAIL
→ capture exact command/status
→ identify first meaningful root cause
→ inspect source/config/dependencies
→ targeted fix
→ rerun failed check
→ rerun affected checks
→ broader verification if shared code changed

Never report overall PASS after a required stage fails.

## Final report

Report:
- PASS / PARTIAL / BLOCKED;
- root cause;
- files changed;
- commands actually executed;
- lint;
- type-check;
- tests;
- architecture validation;
- service startup;
- endpoint/runtime;
- security observations;
- unresolved blockers;
- unverified assumptions.

## Specialized skills

Use:
- `eaos-repository-engineering`
- `eaos-architecture`
- `eaos-safe-modification`
- `eaos-testing`
- `eaos-runtime-debugging`
- `eaos-api-websocket`
- `eaos-security`

The master skill orchestrates; specialized skills provide the detailed procedure.

'@

$Skills[@'
eaos-runtime-debugging
'@] = @'
---
name: eaos-runtime-debugging
description: EAOS runtime troubleshooting skill for FastAPI, Uvicorn, ports, processes, startup/import failures, routing, dependencies, frontend/backend connectivity, and localhost diagnosis.
---

# EAOS Runtime Debugging

## Mission

Diagnose runtime failures from evidence.

Typical failures:
- import error;
- startup exception;
- port conflict;
- wrong bind address;
- process exits;
- route mismatch;
- CORS/origin problem;
- frontend/backend mismatch;
- WebSocket failure;
- dependency unavailable;
- reload-process confusion.

## Runtime model

```text
Browser/UI
→ host + port
→ TCP listener
→ Uvicorn
→ FastAPI
→ middleware
→ router
→ handler
→ application/domain
→ adapter/infrastructure
→ response
```

Find the first broken layer.

## Process

For port 8000:
```powershell
netstat -ano | findstr :8000
```

Do not infer health from the presence of a Uvicorn terminal.

## Port

Confirm:
- expected port;
- actual port;
- bind address;
- conflicting process.

Common EAOS ports:
```text
8000 API
3002 Web UI
3000 possible frontend
7474 Neo4j HTTP
9090 Prometheus
11434 Ollama
```

Treat these as context, not proof of required services.

## Startup logs

Prioritize the earliest meaningful exception:
1. import;
2. configuration;
3. dependency initialization;
4. application factory;
5. route registration;
6. request-time failure.

## Import debugging

For an import error:
```powershell
uv run python -c "import ..."
```

Inspect:
- module path;
- workspace membership;
- package metadata;
- circular imports;
- dependency state.

## Health

Once listening:
```powershell
Invoke-WebRequest http://127.0.0.1:8000/health
```

Verify actual status/body.

## Route debugging

Inspect actual FastAPI routes.

Determine whether `/chat` is:
- HTTP;
- WebSocket;
- streaming;
- UI route;
- another protocol.

Do not assume route existence.

## Dependencies

For Neo4j/Postgres/Ollama/MinIO/Prometheus:
1. determine whether startup requires it;
2. check reachability;
3. inspect configuration;
4. verify credentials/configuration;
5. distinguish optional from mandatory.

## WebSocket diagnosis

For "WebSocket failed", check:
```text
UI host
UI port
API host
API port
WS host
WS port
WS path
ws:// or wss://
proxy
origin/CORS
```

A port mismatch is a configuration problem, not a reason to add arbitrary duplicate listeners.

## Reload

Uvicorn `--reload` may create parent/child processes.

Always verify:
- actual listening port;
- actual request;
- stable application response.

## Fix loop

reproduce
→ capture evidence
→ inspect logs
→ locate root cause
→ patch
→ restart if necessary
→ endpoint test
→ affected tests
→ startup smoke test

Never hide startup exceptions.

## Runtime PASS

Requires:
- process starts;
- expected port listens;
- application initializes;
- required endpoint responds;
- required WebSocket works if applicable;
- expected protocol behavior works.

A crashed process or wrong application on the port is FAIL.

'@

$Skills[@'
eaos-api-websocket
'@] = @'
---
name: eaos-api-websocket
description: EAOS HTTP and WebSocket verification skill for chat endpoints, API/UI port mismatches, routing, CORS, proxying, connection lifecycle, and frontend-backend integration.
---

# EAOS API & WebSocket

## Mission

Verify actual API and WebSocket contracts between EAOS clients and servers.

Never diagnose a WebSocket failure from the browser error alone.

## Protocol discovery

Before testing `/chat`, inspect source and determine whether it is:
- HTTP GET/POST;
- WebSocket;
- streaming;
- SSE;
- UI page;
- proxy route.

Never invent the protocol.

## Route verification

Confirm:
- host;
- port;
- path;
- HTTP method;
- WebSocket path;
- dependencies;
- middleware.

## Port matrix

Use the active environment:
| Component | Host | Port | Protocol |
|---|---|---:|---|
| API | 127.0.0.1 | 8000 | HTTP/WS |
| Web UI | 127.0.0.1 | 3002 | HTTP |
| frontend alternative | 127.0.0.1 | 3000 | HTTP |
| Neo4j | 127.0.0.1 | 7474 | HTTP |
| Prometheus | 127.0.0.1 | 9090 | HTTP |
| Ollama | 127.0.0.1 | 11434 | HTTP |

Only mark a service "required" after inspecting the application.

## HTTP

Verify:
- correct URL;
- correct method;
- status;
- body;
- JSON shape where applicable;
- error contract.

Do not use HEAD as a universal endpoint test.

## WebSocket

Verify:
1. server listening;
2. route registered;
3. correct scheme;
4. correct host;
5. correct port;
6. correct path;
7. origin/proxy policy;
8. handshake;
9. message;
10. response;
11. error behavior;
12. reconnect behavior when required.

## Frontend configuration

Inspect:
```text
ws://
wss://
window.location.host
window.location.hostname
API_BASE_URL
VITE_*
NEXT_PUBLIC_*
environment variables
proxy configuration
```

Prefer one source of truth for API/WS URL configuration.

## CORS

CORS is not a universal explanation for every WebSocket failure.

Inspect actual response/browser evidence.

Do not blindly use wildcard origins.

## Proxy

If UI proxies:
```text
browser
→ UI server
→ proxy
→ API
```

verify each hop.

## Chat

Determine the actual `/chat` contract before testing.

If authentication is required, include it in the test rather than weakening security.

## Failure classification

Classify:
- route absent;
- wrong method;
- wrong port;
- wrong host;
- wrong protocol;
- startup failure;
- import failure;
- proxy failure;
- origin/CORS;
- auth;
- dependency;
- serialization;
- handler;
- lifecycle.

## Evidence

A WebSocket PASS requires:
```text
process running
port listening
route registered
handshake successful
message sent
expected response received
close/error behavior verified when relevant
```

A browser UI without a red error is not sufficient evidence.

## Fix

Fix the actual broken layer:
- URL → configuration;
- missing route → backend route;
- startup → import/config/dependency;
- proxy → proxy config;
- serialization → contract/schema.

Do not create duplicate endpoints merely to mask a client configuration error.

'@

$Skills[@'
eaos-testing
'@] = @'
---
name: eaos-testing
description: EAOS testing and verification skill for pytest, regression tests, API/WebSocket tests, architecture tests, failure diagnosis, and rerun strategy.
---

# EAOS Testing and Verification

## Mission

Tests must prove behavior. A passing command is useful only when the tests themselves exercise the intended contract.

## Testing hierarchy

Use as appropriate:
```text
unit
→ component/integration
→ architecture validation
→ runtime verification
→ regression
```

## Before fixing a bug

1. Find existing tests.
2. Reproduce failure when practical.
3. Determine expected behavior.
4. Determine actual behavior.
5. Add/update a meaningful regression test.

A good regression test should fail for the old behavior and pass for the corrected behavior.

## Run configured tests

Use:
```powershell
uv run task test
```

or:
```powershell
uv run pytest tests/
```

Include `fitness/` when configured as part of acceptance.

Record:
- collected;
- passed;
- failed;
- skipped;
- errors;
- exit code.

## Failure classification

Classify failures as:
- implementation defect;
- test defect;
- fixture defect;
- environment defect;
- dependency defect;
- nondeterminism;
- contract mismatch.

Trace:
```text
test
→ assertion/error
→ fixture/input
→ implementation
→ configuration/dependency
→ root cause
```

## Never hide failures

Do not:
- delete tests;
- skip tests without documented reason;
- weaken assertions;
- swallow exceptions;
- disable strict checks;
- add blanket ignores;
- increase timeouts without root-cause analysis.

## Async/WebSocket tests

Verify:
1. route;
2. server startup;
3. connection;
4. message acceptance;
5. expected response;
6. invalid input;
7. close/error behavior.

Prefer synchronization primitives over arbitrary sleeps.

## API tests

Verify:
- correct method;
- status code;
- response shape;
- validation;
- authentication/authorization where relevant;
- meaningful side effects;
- dependency failures.

Do not test only "does not crash".

## Rerun policy

Local change:
- failing test;
- affected tests.

Shared package:
- affected tests;
- integration tests;
- architecture validation if boundaries changed.

Core/kernel/runtime:
- relevant tests;
- full suite when practical;
- architecture validation;
- runtime smoke test.

API/WebSocket:
- unit;
- API/WS tests;
- startup;
- real endpoint checks.

## Test quality

Watch for:
- empty assertions;
- excessive mocking;
- private implementation coupling;
- arbitrary sleeps;
- environment-only assumptions;
- swallowed exceptions.

## Final evidence

Report exact command and observed outcome. Do not say "tests look good".

Example:
```text
uv run pytest tests/
exit code: 0
collected: N
passed: N
failed: 0
```

Only use numbers actually observed.

'@

$Skills[@'
eaos-security
'@] = @'
---
name: eaos-security
description: EAOS security engineering skill for autonomous code modification, command execution, filesystem safety, APIs, WebSockets, secrets, databases, Docker, dependencies, and MCP integrations.
---

# EAOS Security Engineering

## Mission

Keep autonomous repository engineering bounded by explicit security controls.

## Review priorities

Check:
1. secrets;
2. command execution;
3. filesystem mutation;
4. path traversal;
5. subprocess;
6. network exposure;
7. authentication;
8. authorization;
9. WebSocket exposure;
10. database access;
11. Docker;
12. dependencies;
13. MCP permissions;
14. unsafe deserialization;
15. sensitive logging.

## Secrets

Never commit or generate real credentials.

Look for:
- API keys;
- passwords;
- tokens;
- private keys;
- credential-bearing database URLs;
- cloud credentials;
- accidental `.env` commits.

Never print secrets in debugging output. Redact them in reports.

## Command execution

Treat:
```text
subprocess
os.system
shell=True
PowerShell
cmd.exe
```
as security-sensitive.

Review input control, shell interpolation, executable allowlists, working directory, environment, privileges, and output handling.

Prefer argument arrays over shell strings.

## Filesystem

Review:
- user-controlled paths;
- traversal;
- symlinks;
- archive extraction;
- arbitrary writes;
- cleanup;
- generated files.

Apply the safe-modification protected-path policy.

## API

Check:
- authentication;
- authorization;
- validation;
- rate limiting where appropriate;
- error leakage;
- CORS;
- debug exposure;
- administrative endpoints.

Do not use wildcard CORS as a blind production fix.

## WebSocket

Review:
- authentication at handshake;
- authorization per operation;
- origin policy;
- message validation;
- resource exhaustion;
- connection limits/timeouts;
- error leakage;
- command execution through agent/chat channels.

## Database

For Neo4j/Postgres/SQLAlchemy:
- parameterize queries;
- avoid string-built queries from user input;
- least privilege;
- safe migrations;
- safe credentials;
- no automatic destructive reset.

## Docker

Review:
- exposed ports;
- privileged mode;
- host mounts;
- secrets;
- root execution;
- unnecessary services;
- network exposure.

Never use destructive Docker cleanup as routine repair.

## MCP

Treat MCP tools as privileged capabilities.

For mutating tools:
- prefer approval/Ask semantics when appropriate;
- verify scope;
- minimize permissions;
- report mutations.

A tool being available does not mean every operation should be automatically allowed.

## Dependencies

For dependency changes:
- use `uv` lock/sync;
- avoid unnecessary packages;
- inspect significant additions;
- run tests;
- perform security checks when available.

Do not upgrade unrelated dependencies opportunistically.

## Severity

Consider:
- impact;
- exploitability;
- exposure;
- privilege;
- affected assets;
- likelihood;
- compensating controls.

Do not label every warning critical.

## Security fix workflow

finding
→ validate
→ root cause
→ minimal secure fix
→ regression test
→ security check
→ lint/type/test
→ runtime verification

## Autonomous boundary

Do not allow autonomy to become:
- arbitrary command execution from untrusted input;
- unrestricted filesystem mutation;
- unrestricted database mutation;
- credential disclosure;
- hidden privilege escalation;
- hidden persistence.

## Final report

Report:
- finding;
- evidence;
- severity;
- root cause;
- fix;
- files changed;
- verification;
- residual risk.

State exactly what remains unverified.

'@

$Skills[@'
eaos-safe-modification
'@] = @'
---
name: eaos-safe-modification
description: Safety and mutation-control skill for EAOS. Use before repository-wide edits, automated fixes, cleanup, generated changes, backup-sensitive work, or infrastructure mutations.
---

# EAOS Safe Modification

## Mission

Enable autonomous engineering without damaging EAOS backups, virtual environments, Git metadata, or persistent data.

## Protected paths

Never intentionally modify:
```text
D:\EAOS\eaos_backups\
D:\EAOS\.venv\
D:\EAOS\.eaos_backups\
D:\EAOS\.eaos_contract_backup_*\
D:\EAOS\.eaos-repair-backup\
D:\EAOS\.git\
```

Discover additional backup directories before broad automated changes.

## Protected operations

Do not delete, overwrite, move, rename, clean, format, or bulk-rewrite protected content.

Do not assume a command is safe merely because the visible argument does not contain a protected path.

## Broad commands

Before:
```powershell
ruff check --fix .
ruff format .
```

verify configuration exclusions and source scope.

Prefer explicit source roots if exclusions are ambiguous.

After broad fixes:
```powershell
git status --short
git diff --stat
git diff
```

Inspect unexpected changes.

## Never use as automatic repair

Do not automatically run:
```text
git clean -fd
git clean -fdx
docker compose down -v
docker system prune
docker volume prune
Remove-Item -Recurse -Force
```

unless the user explicitly authorizes the destructive operation.

## Git safety

Before mutation:
```powershell
git status --short
git diff --stat
```

After mutation:
```powershell
git status --short
git diff --stat
```

Never discard unrelated user changes.

If a target file already has modifications, inspect them before editing.

## Backup policy

Backups are protected assets, not disposable build artifacts.

Never:
- clean backups;
- format backups;
- mass-refactor backups;
- rename backups for convenience;
- include backups in automated repair.

## `.venv`

Do not edit files inside `.venv`.

Use:
```powershell
uv sync
```
instead of manual environment modification.

## Docker/data safety

Inspect compose configuration before starting infrastructure.

Do not drop/reset databases or volumes automatically.

## Safe patch rule

Prefer the smallest correct change.

If an automated operation wants to rewrite a large unrelated area, stop and inspect.

## Verification after mutation

Every meaningful mutation should be followed by:
1. diff inspection;
2. targeted validation;
3. affected tests;
4. broader verification when shared code changed.

## Stop conditions

Stop if:
- protected content may be modified;
- destructive action is required;
- user changes may be overwritten;
- command scope is unclear;
- a tool wants to rewrite unrelated files;
- data destruction appears necessary.

Safety is a prerequisite for autonomous operation.

'@


foreach ($name in $Skills.Keys) {
    $skillDir = Join-Path $SkillsRoot $name
    $skillFile = Join-Path $skillDir 'SKILL.md'

    New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
    Write-Utf8NoBom -Path $skillFile -Content ([string]$Skills[$name])

    $bytes = [IO.File]::ReadAllBytes($skillFile)
    $hasBom = $bytes.Length -ge 3 -and
        $bytes[0] -eq 0xEF -and
        $bytes[1] -eq 0xBB -and
        $bytes[2] -eq 0xBF

    if ($hasBom) {
        throw "UTF-8 BOM detected in $skillFile"
    }

    Write-Host "PASS  $skillFile"
}

Write-Host ''
Write-Host 'EAOS Antigravity skill installation completed.'
Write-Host "Root: $SkillsRoot"
Write-Host ''
Get-ChildItem -LiteralPath $SkillsRoot -Directory |
    Sort-Object Name |
    ForEach-Object {
        $skillFile = Join-Path $_.FullName 'SKILL.md'
        if (Test-Path -LiteralPath $skillFile) {
            Write-Host "  [OK] $($_.Name)\SKILL.md"
        }
    }
