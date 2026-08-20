"""Tests for the rebuilt AIDE application boundary."""

from pathlib import Path

from apps.aide.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_aide_app_imports_and_registers_workspace_routes() -> None:
    """AIDE imports independently and registers application routes."""

    paths = {getattr(route, "path", None) for route in app.routes}
    for route in app.routes:
        nested = getattr(getattr(route, "original_router", None), "routes", [])
        paths.update(getattr(item, "path", None) for item in nested)
    assert "/" in paths
    assert "/workspace/state" in paths
    assert "/integrations/gateway/health" in paths
    assert "/static" in paths


def test_workspace_template_and_static_load() -> None:
    """The IDE shell renders and loads AIDE-owned static assets."""

    response = client.get("/")
    assert response.status_code == 200
    assert "EAOS" in response.text
    assert "monaco-editor" in response.text
    assert "copilot-pane" in response.text
    static_response = client.get("/static/js/core/main.js")
    assert static_response.status_code == 200
    assert "mountEditor" in static_response.text
    assert "observeGateway" in static_response.text


def test_workspace_state_declares_gateway_contracts() -> None:
    """AIDE consumes Gateway contracts without owning backend capability."""

    response = client.get("/workspace/state")
    assert response.status_code == 200
    state = response.json()
    contracts = {item["name"]: item for item in state["capabilities"]}
    assert state["api_base_url"] == "http://127.0.0.1:8000"
    assert contracts["agents"]["owner"] == "apps/api"
    assert contracts["chat-stream"]["transport"] == "WebSocket"
    assert contracts["telemetry"]["endpoint"].endswith("/telemetry/ingest")


def test_required_aide_modules_exist_and_main_stays_bootstrap_only() -> None:
    """AIDE JS capability modules are split by responsibility."""

    root = Path("apps/aide/static/js")
    expected = [
        "core/main.js",
        "core/state.js",
        "core/gateway.js",
        "core/websocket.js",
        "editor/monaco.js",
        "explorer/tree.js",
        "terminal/terminal.js",
        "chat/chat.js",
        "agent/status.js",
        "git/git.js",
        "github/github.js",
        "runtime/runtime.js",
        "telemetry/telemetry.js",
        "workspace/layout.js",
        "ide/inspector.js",
        "agent/tasks.js",
    ]
    for relative_path in expected:
        assert (root / relative_path).exists()

    main_js = (root / "core/main.js").read_text(encoding="utf-8")
    assert main_js.count("function ") == 0
    assert "new WebSocket" not in main_js


def test_no_aide_backend_api_boundary_was_created() -> None:
    """AIDE must not duplicate the Gateway API boundary."""

    assert not Path("apps/aide/api").exists()


def test_workspace_does_not_claim_backend_success_without_probe() -> None:
    """AIDE labels backend state as unknown until it observes Gateway state."""

    response = client.get("/")
    assert response.status_code == 200
    assert "GATEWAY UNKNOWN" in response.text
    assert "SYSTEM READY" not in response.text


def test_gateway_health_probe_contract_shape() -> None:
    """Gateway probe reports observation state rather than fake health."""

    response = client.get("/integrations/gateway/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] in {"observed", "degraded", "unavailable"}
    assert payload["target"].endswith("/health")


def test_gateway_contracts_classify_real_and_missing_capabilities() -> None:
    """AIDE exposes discovered Gateway contracts and explicit gaps."""

    response = client.get("/integrations/gateway/contracts")
    assert response.status_code == 200
    contracts = {item["name"]: item for item in response.json()}
    assert contracts["health"]["path"] == "/health"
    assert contracts["task-submission"]["path"] == "/api/v1/control/execute"
    assert contracts["task-status"]["state"] == "available"
    assert contracts["task-status"]["path"] == "/api/v1/tasks/{task_id}"
    assert contracts["lifecycle-event-stream"]["state"] == "available"


def test_gateway_snapshot_preserves_unavailable_and_missing_states() -> None:
    """AIDE does not fake lifecycle or evidence success when Gateway is down."""

    response = client.get("/integrations/gateway/snapshot")
    assert response.status_code == 200
    snapshot = {item["contract"]: item for item in response.json()}
    assert snapshot["health"]["status"] in {"available", "degraded", "unavailable"}


def test_task_submission_requires_real_command() -> None:
    """AIDE task interaction rejects empty commands instead of faking execution."""

    response = client.post("/interactions/tasks", json={"command": ""})
    assert response.status_code == 200
    payload = response.json()
    assert payload["contract"] == "task-submission"
    assert payload["status"] == "degraded"


def test_aide_task_modules_consume_gateway_lifecycle_contracts() -> None:
    tasks_js = Path("apps/aide/static/js/agent/tasks.js").read_text(encoding="utf-8")
    ws_js = Path("apps/aide/static/js/core/websocket.js").read_text(encoding="utf-8")
    assert "ACCEPTED" in tasks_js
    assert "COMPLETED" in tasks_js
    assert "QUEUED" not in tasks_js
    assert "TIMEOUT" not in tasks_js
    assert "CANCELLED" not in tasks_js
    assert "renderTaskState" in tasks_js
    assert "/api/v1/tasks/${taskId}/events" in ws_js
    assert "apps/aide/api" not in tasks_js


def test_phase7_engineering_ux_surfaces_are_client_only() -> None:
    template = Path("apps/aide/templates/workspace.html").read_text(encoding="utf-8")
    main_js = Path("apps/aide/static/js/core/main.js").read_text(encoding="utf-8")
    editor_js = Path("apps/aide/static/js/editor/monaco.js").read_text(encoding="utf-8")
    explorer_js = Path("apps/aide/static/js/explorer/tree.js").read_text(encoding="utf-8")
    git_js = Path("apps/aide/static/js/git/git.js").read_text(encoding="utf-8")
    terminal_js = Path("apps/aide/static/js/terminal/terminal.js").read_text(encoding="utf-8")

    assert 'id="task-ux"' in template
    assert 'id="event-timeline"' in template
    assert "mountTaskUx" in main_js
    assert "onSelect: editor.openFile" in main_js
    assert "markChanged" in editor_js
    assert "markSaved" in editor_js
    assert "loading" in explorer_js
    assert "error" in explorer_js
    assert "destructiveOperations: false" in git_js
    assert "backendExecution: false" in terminal_js
    assert "apps/aide/api" not in "".join([template, main_js, editor_js, explorer_js, git_js, terminal_js])


def test_phase7_websocket_lifecycle_regressions_are_real_gateway_contracts() -> None:
    ws_js = Path("apps/aide/static/js/core/websocket.js").read_text(encoding="utf-8")
    tasks_js = Path("apps/aide/static/js/agent/tasks.js").read_text(encoding="utf-8")
    inspector_js = Path("apps/aide/static/js/ide/inspector.js").read_text(encoding="utf-8")

    assert "new WebSocket" in ws_js
    assert "createLifecycleEventBuffer" in ws_js
    assert "seen.has" in ws_js
    assert "events.push(event)" in ws_js
    assert "events.sort" not in ws_js
    assert "event.code === 1000" in ws_js
    assert "onError" in ws_js
    assert "completed" in tasks_js
    assert "failed" in tasks_js
    assert "denied" in tasks_js
    assert "verification" in inspector_js
    assert "evidence_ref" in inspector_js
    assert "correlation_id" in inspector_js
    assert "QUEUED" not in tasks_js
    assert "TIMEOUT" not in tasks_js
    assert "CANCELLED" not in tasks_js
    assert "success" not in tasks_js.lower()


def test_phase_7_1_workspace_wires_command_submission_to_single_pipeline() -> None:
    """The browser contract submits through AIDE interaction route and then opens Gateway WS."""

    template = Path("apps/aide/templates/workspace.html").read_text(encoding="utf-8")
    main_js = Path("apps/aide/static/js/core/main.js").read_text(encoding="utf-8")
    tasks_js = Path("apps/aide/static/js/agent/tasks.js").read_text(encoding="utf-8")
    chat_js = Path("apps/aide/static/js/chat/chat.js").read_text(encoding="utf-8")

    assert 'id="task-form"' in template
    assert 'id="task-command"' in template
    assert "fetch('/interactions/tasks'" in tasks_js
    assert "connect(payload.task_id)" in tasks_js
    assert "onSubmitCommand(command)" in main_js
    assert "taskUx.submit(command)" in main_js
    assert "options.onSubmitCommand?.(command)" in chat_js
    assert "task_" not in tasks_js.replace("task_id", "")


def test_phase_7_1_lifecycle_events_share_task_inspector_runtime_pipeline() -> None:
    """Task panel, inspector, and runtime footer are synchronized from one event stream."""

    main_js = Path("apps/aide/static/js/core/main.js").read_text(encoding="utf-8")
    tasks_js = Path("apps/aide/static/js/agent/tasks.js").read_text(encoding="utf-8")
    inspector_js = Path("apps/aide/static/js/ide/inspector.js").read_text(encoding="utf-8")
    runtime_js = Path("apps/aide/static/js/runtime/runtime.js").read_text(encoding="utf-8")

    assert "onTaskState(payload)" in main_js
    assert "updateTaskInspector(inspectorNodes" in main_js
    assert "runtimeNodes.task.textContent" in main_js
    assert "renderPayload(event)" in tasks_js
    assert "renderEvent(event)" in tasks_js
    assert "verificationText" in tasks_js
    assert "classifyTaskOutcome" in tasks_js
    assert "payload.verification?.passed" in inspector_js
    assert "SYSTEM READY" not in runtime_js


def test_phase_7_1_websocket_duplicate_terminal_and_reconnect_contract() -> None:
    """WS client ignores duplicate/unsupported events and bounds reconnect before terminal."""

    ws_js = Path("apps/aide/static/js/core/websocket.js").read_text(encoding="utf-8")
    tasks_js = Path("apps/aide/static/js/agent/tasks.js").read_text(encoding="utf-8")

    assert "VALID_STATES.has" in ws_js
    assert "seen.has" in ws_js
    assert "events.push(event)" in ws_js
    assert "events.sort" not in ws_js
    assert "maxReconnects" in ws_js
    assert "terminal || event.code === 1000" in ws_js
    assert "clearTimeout" in ws_js
    assert "RUNTIME_STATES.has" in tasks_js
    assert "return false" in tasks_js
    for prohibited_state in ("QUEUED", "TIMEOUT", "CANCELLED"):
        assert prohibited_state not in tasks_js
        assert prohibited_state not in ws_js


def test_phase_7_1_gateway_lifecycle_outcomes_render_real_task_ids() -> None:
    """The Gateway contract returns real task IDs for completed, denied, and failed outcomes."""

    from apps.api.app.main import app as gateway_app

    gateway_client = TestClient(gateway_app)
    outcomes = {
        "doctor": "completed",
        "deny this request": "denied",
        "fail": "failed",
        "verify-fail": "failed",
    }
    for command, expected_state in outcomes.items():
        response = gateway_client.post("/api/v1/control/execute", json={"command": command})
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == expected_state
        assert payload["task_id"].startswith("task_")
        assert payload["lifecycle_state"] == expected_state
        assert payload["task_id"] == payload["metadata"]["correlation_id"]


def test_phase_reuse_docs_define_aide_as_human_gateway_not_runtime() -> None:
    """Architecture docs classify reuse and forbid rebuilding EAOS inside AIDE."""

    matrix = Path("apps/aide/docs/eaos_reuse_matrix.md").read_text(encoding="utf-8")
    architecture = Path("apps/aide/docs/human_gateway_architecture.md").read_text(encoding="utf-8")

    assert "Capability | Existing owner | Existing contract" in matrix
    assert "Task lifecycle events" in matrix
    assert "WS /api/v1/tasks/{task_id}/events" in matrix
    assert "DXS / Digital Twin Structure" in matrix
    assert "D. CONTRACT GAP" in matrix
    assert "AIDE does not implement DXS" in matrix
    assert "AIDE is not EAOS" in architecture
    assert "AIDE is not the execution engine" in architecture
    assert "AIDE is not DXS" in architecture
    assert "EAOS must continue to operate when AIDE is stopped" in architecture


def test_phase_reuse_boundary_prevents_aide_from_absorbing_eaos_engines() -> None:
    """AIDE remains a thin consumer and does not import or instantiate EAOS engines."""

    source_roots = [Path("apps/aide/app"), Path("apps/aide/static"), Path("apps/aide/templates")]
    aide_paths = [path for root in source_roots for path in root.rglob("*") if path.is_file()]
    aide_text = "\n".join(
        path.read_text(encoding="utf-8") for path in aide_paths if path.suffix in {".py", ".js", ".html"}
    )

    forbidden_fragments = [
        "from engine.sandbox",
        "WASMSandboxRuntime(",
        "EnterpriseDigitalTwinOrchestrator(",
        "DigitalTwinOrchestrator(",
        "SelfHealingLoopAdapter(",
        "MerkleLedgerVerifier(",
        "NativeRegoCompiler(",
        "InMemoryMemoryRepository(",
        "task_lifecycle_service =",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in aide_text

    assert not Path("apps/aide/api").exists()
    assert "/api/v1/control/execute" in aide_text
    assert "/api/v1/tasks/{task_id}" in aide_text
    assert "/api/v1/tasks/${taskId}/events" in aide_text


def test_phase_reuse_gateway_remains_authoritative_without_aide() -> None:
    """The Gateway task lifecycle works directly without running through AIDE."""

    from apps.api.app.main import app as gateway_app

    gateway_client = TestClient(gateway_app)
    created = gateway_client.post("/api/v1/control/execute", json={"command": "doctor"}).json()
    task_id = created["task_id"]
    status = gateway_client.get(f"/api/v1/tasks/{task_id}").json()

    assert created["lifecycle_state"] == "completed"
    assert status["task_id"] == task_id
    assert status["correlation_id"] == task_id
    assert status["evidence"]["task_id"] == task_id
    assert status["verification"]["passed"] is True
    assert status["governance"]["result"] in {"allowed", "denied"}


def test_phase_reuse_task_panel_renders_verification_metadata() -> None:
    """Task panel exposes Gateway verification metadata without local verification."""

    template = Path("apps/aide/templates/workspace.html").read_text(encoding="utf-8")
    tasks_js = Path("apps/aide/static/js/agent/tasks.js").read_text(encoding="utf-8")
    main_js = Path("apps/aide/static/js/core/main.js").read_text(encoding="utf-8")

    assert 'id="verification-result"' in template
    assert "verificationText(payload)" in tasks_js
    assert "nodes.verification.textContent" in tasks_js
    assert "document.getElementById('verification-result')" in main_js


def test_phase8_aide_consumes_gateway_capability_registry_without_backend() -> None:
    """AIDE exposes a thin capability-registry adapter and browser renderer only."""

    response = client.get("/integrations/gateway/capabilities")
    assert response.status_code == 200
    payload = response.json()
    assert payload["contract"] == "capability-registry"
    assert payload["status"] in {"available", "degraded", "unavailable"}

    template = Path("apps/aide/templates/workspace.html").read_text(encoding="utf-8")
    main_js = Path("apps/aide/static/js/core/main.js").read_text(encoding="utf-8")
    contracts_js = Path("apps/aide/static/js/runtime/contracts.js").read_text(encoding="utf-8")
    capabilities_js = Path("apps/aide/static/js/runtime/capabilities.js").read_text(encoding="utf-8")

    assert 'id="capability-registry"' in template
    assert "loadCapabilityRegistry" in contracts_js
    assert "fetch('/integrations/gateway/capabilities')" in contracts_js
    assert "renderCapabilityRegistry(capabilitiesNode, envelope)" in main_js
    assert "data-capability-status" in capabilities_js
    assert "contract_gap" not in capabilities_js


def test_phase8_aide_renders_unavailable_registry_without_fake_ready_state() -> None:
    """AIDE defaults registry presentation to unavailable, not ready/healthy/success."""

    template = Path("apps/aide/templates/workspace.html").read_text(encoding="utf-8")
    capabilities_js = Path("apps/aide/static/js/runtime/capabilities.js").read_text(encoding="utf-8")

    assert 'data-capability-registry-status="unavailable"' in template
    assert "Registry unavailable" in template
    assert "unavailable" in capabilities_js
    for fake_state in ("ready", "healthy", "success"):
        assert fake_state not in capabilities_js.lower()


def test_phase8_aide_keeps_dxs_and_engine_imports_out_of_source() -> None:
    """AIDE consumes Gateway contracts and does not import DXS/runtime internals."""

    source_roots = [Path("apps/aide/app"), Path("apps/aide/static"), Path("apps/aide/templates")]
    source_text = "\n".join(
        path.read_text(encoding="utf-8")
        for root in source_roots
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".py", ".js", ".html"}
    )

    forbidden = [
        "import digitaltwin",
        "from digitaltwin",
        "tools.digital_twin",
        "WASMSandboxRuntime(",
        "NativeRegoCompiler(",
        "MerkleLedgerVerifier(",
        "SelfHealingLoopAdapter(",
        "InMemoryMemoryRepository(",
    ]
    for fragment in forbidden:
        assert fragment not in source_text
    assert not Path("apps/aide/api").exists()
