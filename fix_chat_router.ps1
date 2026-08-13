$ErrorActionPreference = "Stop"

$Root = (Get-Location).Path
$Chat = Join-Path $Root "apps\api\app\routers\chat.py"
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Backup = "$Chat.bak_$Stamp"

Write-Host ""
Write-Host "EAOS Chat Router Repair"
Write-Host "======================="

if (-not (Test-Path $Chat)) {
    throw "Missing file: $Chat"
}

Write-Host "[1/8] Backing up chat.py..."
Copy-Item $Chat $Backup -Force
Write-Host "BACKUP: $Backup"

Write-Host "[2/8] Writing UTF-8 No BOM chat.py..."

$content = @'
"""Chat router for the EAOS AI Studio."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from runtime.state.task_lifecycle import TaskState

from apps.api.app.routers.runtime_control_router import control_plane
from apps.api.app.services.chat.orchestrator import ChatOrchestrator

router = APIRouter(tags=["AI Studio Core"])

PROJECT_ROOT = Path(__file__).resolve().parents[4]
orchestrator = ChatOrchestrator(PROJECT_ROOT)


@router.get("/chat", response_class=HTMLResponse)
async def chat_page() -> HTMLResponse:
    """Serve the EAOS AI Studio chat page."""
    return HTMLResponse(
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >
    <title>EAOS AI Studio</title>
    <style>
        body {
            font-family: system-ui, sans-serif;
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 20px;
        }

        h1 {
            margin-bottom: 20px;
        }

        #output {
            min-height: 400px;
            padding: 16px;
            border: 1px solid #ccc;
            border-radius: 8px;
            white-space: pre-wrap;
            overflow: auto;
        }

        .controls {
            display: flex;
            gap: 8px;
            margin-top: 16px;
        }

        #message {
            flex: 1;
            padding: 10px;
        }

        button {
            padding: 10px 18px;
            cursor: pointer;
        }

        #status {
            margin-bottom: 12px;
        }
    </style>
</head>
<body>
    <h1>EAOS AI Studio</h1>

    <div id="status">Connecting...</div>

    <pre id="output"></pre>

    <div class="controls">
        <input
            id="message"
            type="text"
            placeholder="Enter your message"
            autocomplete="off"
        >
        <button id="send">Send</button>
    </div>

    <script>
        const statusElement = document.getElementById("status");
        const outputElement = document.getElementById("output");
        const messageElement = document.getElementById("message");
        const sendButton = document.getElementById("send");

        const protocol =
            window.location.protocol === "https:" ? "wss:" : "ws:";

        const socketUrl =
            protocol + "//" + window.location.host + "/ws/chat";

        const socket = new WebSocket(socketUrl);

        function writeOutput(data) {
            outputElement.textContent +=
                JSON.stringify(data, null, 2) + "\\n\\n";
            outputElement.scrollTop = outputElement.scrollHeight;
        }

        socket.onopen = function () {
            statusElement.textContent = "WebSocket connected";
        };

        socket.onmessage = function (event) {
            try {
                writeOutput(JSON.parse(event.data));
            } catch (error) {
                outputElement.textContent += event.data + "\\n";
            }
        };

        socket.onerror = function () {
            statusElement.textContent =
                "WebSocket connection error";
        };

        socket.onclose = function () {
            statusElement.textContent =
                "WebSocket disconnected";
        };

        function sendMessage() {
            const message = messageElement.value.trim();

            if (!message) {
                return;
            }

            if (socket.readyState !== WebSocket.OPEN) {
                statusElement.textContent =
                    "WebSocket is not connected";
                return;
            }

            socket.send(
                JSON.stringify({
                    conversation_id: "conv-web-chat",
                    message: message,
                    agent_role: "coder",
                    system_instruction: "",
                    active_file: "apps/api/app/routers/chat.py",
                    temperature: 0.7,
                    max_output_tokens: 4096,
                    json_mode: false
                })
            );

            messageElement.value = "";
        }

        sendButton.addEventListener("click", sendMessage);

        messageElement.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                sendMessage();
            }
        });
    </script>
</body>
</html>
        """
    )


async def _safe_send(
    websocket: WebSocket,
    payload: dict[str, Any],
) -> bool:
    """Send a WebSocket payload unless the client has disconnected."""
    try:
        await websocket.send_json(payload)
    except (WebSocketDisconnect, RuntimeError):
        return False

    return True


def _lifecycle_payload(
    state: TaskState,
    ctx: Any,
) -> dict[str, Any]:
    """Build a lifecycle event payload."""
    return {
        "type": "task_lifecycle",
        "state": state.value,
        "correlation": ctx.__dict__,
        "proof_hash": ctx.generate_proof_hash(),
    }


@router.websocket("/ws/chat")
async def websocket_chat_endpoint(
    websocket: WebSocket,
) -> None:
    """Handle AI Studio chat requests through runtime lifecycle."""
    await websocket.accept()

    try:
        while True:
            raw = await websocket.receive_text()
            data: dict[str, Any] = json.loads(raw)

            conversation_id = str(
                data.get("conversation_id", "conv-001")
            )
            agent_role = str(
                data.get("agent_role", "agent-coder")
            )

            fsm, ctx = control_plane.create_task(
                user_request_id=conversation_id,
                agent_id=agent_role,
            )

            fsm.transition_to(
                TaskState.QUEUED,
                f"TOKEN-QUEUE-{ctx.task_id}",
            )

            if not await _safe_send(
                websocket,
                _lifecycle_payload(TaskState.QUEUED, ctx),
            ):
                return

            fsm.transition_to(
                TaskState.RUNNING,
                f"TOKEN-RUN-{ctx.task_id}",
            )

            if not await _safe_send(
                websocket,
                _lifecycle_payload(TaskState.RUNNING, ctx),
            ):
                return

            try:
                async for event in orchestrator.process_goal(
                    conversation_id=conversation_id,
                    message=str(data.get("message", "")),
                    system_instruction=str(
                        data.get("system_instruction", "")
                    ),
                    active_file=str(
                        data.get(
                            "active_file",
                            "apps/api/app/routers/chat.py",
                        )
                    ),
                    temperature=float(
                        data.get("temperature", 0.7)
                    ),
                    max_output_tokens=int(
                        data.get("max_output_tokens", 4096)
                    ),
                    json_mode=bool(
                        data.get("json_mode", False)
                    ),
                ):
                    event["task_id"] = ctx.task_id
                    event["proof_hash"] = (
                        ctx.generate_proof_hash()
                    )

                    if not await _safe_send(
                        websocket,
                        event,
                    ):
                        return

                fsm.transition_to(
                    TaskState.VERIFYING,
                    f"TOKEN-VERIFY-{ctx.task_id}",
                )

                if not await _safe_send(
                    websocket,
                    _lifecycle_payload(TaskState.VERIFYING, ctx),
                ):
                    return

                fsm.transition_to(
                    TaskState.COMPLETED,
                    f"TOKEN-COMPLETE-{ctx.task_id}",
                )

                if not await _safe_send(
                    websocket,
                    _lifecycle_payload(TaskState.COMPLETED, ctx),
                ):
                    return

            except WebSocketDisconnect:
                return

            except Exception as exc:
                failure, outcome = (
                    control_plane.handle_runtime_failure(
                        ctx.task_id,
                        exc,
                        "chat_orchestrator",
                    )
                )

                await _safe_send(
                    websocket,
                    {
                        "type": "task_lifecycle",
                        "state": fsm.current_state.value,
                        "correlation": ctx.__dict__,
                        "proof_hash": ctx.generate_proof_hash(),
                        "failure": failure.__dict__,
                        "recovery_outcome": outcome.__dict__,
                    },
                )

    except WebSocketDisconnect:
        return

    except json.JSONDecodeError:
        await _safe_send(
            websocket,
            {
                "type": "error",
                "error": "Invalid JSON request.",
            },
        )
    except RuntimeError:
        return
'@

[System.IO.File]::WriteAllText(
    $Chat,
    $content,
    [System.Text.UTF8Encoding]::new($false)
)

Write-Host "CREATED: $Chat"

Write-Host "[3/8] Checking UTF-8 BOM..."
$bytes = [System.IO.File]::ReadAllBytes($Chat)

if (
    $bytes.Length -ge 3 -and
    $bytes[0] -eq 0xEF -and
    $bytes[1] -eq 0xBB -and
    $bytes[2] -eq 0xBF
) {
    throw "UTF-8 BOM detected."
}

Write-Host "UTF-8 No BOM: OK"

Write-Host "[4/8] Checking Python import..."
.\.venv\Scripts\python.exe -c `
    "from apps.api.app.routers.chat import websocket_chat_endpoint; print('IMPORT OK')"

if ($LASTEXITCODE -ne 0) {
    throw "chat.py import failed."
}

Write-Host "[5/8] Running Ruff..."
.\.venv\Scripts\python.exe -m ruff check `
    apps/api/app/routers/chat.py `
    apps/api/app/services/chat

if ($LASTEXITCODE -ne 0) {
    throw "Ruff failed."
}

Write-Host "[6/8] Running unit tests..."
.\.venv\Scripts\python.exe -m pytest tests/unit -q

if ($LASTEXITCODE -ne 0) {
    throw "Unit tests failed."
}

Write-Host "[7/8] Checking verification subsystem..."
.\.venv\Scripts\python.exe -c @"
import asyncio
from pathlib import Path

from apps.api.app.services.chat.verification.coordinator import (
    VerificationCoordinator,
)

async def main():
    coordinator = VerificationCoordinator(Path.cwd())

    events = []

    async for event in coordinator.run():
        events.append(event)

    print("VERIFICATION EVENTS:")
    for event in events:
        print(event["type"])

    print("VERIFICATION COORDINATOR OK")

asyncio.run(main())
"@

if ($LASTEXITCODE -ne 0) {
    throw "Verification coordinator check failed."
}

Write-Host "[8/8] Final architecture checks..."

$legacy = Join-Path `
    $Root `
    "apps\api\app\services\chat\verification_pipeline.py"

if (Test-Path $legacy) {
    throw "Legacy verification_pipeline.py still exists."
}

Write-Host ""
Write-Host "======================================"
Write-Host "CHAT ROUTER REPAIR PASSED"
Write-Host "======================================"
Write-Host ""
Write-Host "Backup:"
Write-Host "  $Backup"
Write-Host ""
Write-Host "Architecture:"
Write-Host "  chat.py"
Write-Host "      -> ChatOrchestrator"
Write-Host "      -> VerificationCoordinator"
Write-Host "      -> RuffRunner / PytestRunner"
Write-Host "      -> ResultAggregator"
Write-Host "      -> EvidenceStore"
Write-Host ""
Write-Host "WebSocket lifecycle:"
Write-Host "  QUEUED"
Write-Host "    -> RUNNING"
Write-Host "    -> LLM STREAM"
Write-Host "    -> VERIFICATION"
Write-Host "    -> VERIFYING"
Write-Host "    -> COMPLETED"
Write-Host ""
Write-Host "Disconnect safety: ENABLED"
Write-Host "UTF-8 No BOM: VERIFIED"