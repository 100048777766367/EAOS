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
    assert contracts["task-status"]["state"] == "missing"
    assert contracts["lifecycle-event-stream"]["state"] == "missing"


def test_gateway_snapshot_preserves_unavailable_and_missing_states() -> None:
    """AIDE does not fake lifecycle or evidence success when Gateway is down."""

    response = client.get("/integrations/gateway/snapshot")
    assert response.status_code == 200
    snapshot = {item["contract"]: item for item in response.json()}
    assert snapshot["task-status"]["status"] == "missing"
    assert snapshot["lifecycle-event-stream"]["status"] == "missing"
    assert snapshot["health"]["status"] in {"available", "degraded", "unavailable"}


def test_task_submission_requires_real_command() -> None:
    """AIDE task interaction rejects empty commands instead of faking execution."""

    response = client.post("/interactions/tasks", json={"command": ""})
    assert response.status_code == 200
    payload = response.json()
    assert payload["contract"] == "task-submission"
    assert payload["status"] == "degraded"
