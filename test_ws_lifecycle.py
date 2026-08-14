import json
import time

from apps.api.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

print("=== WS TASK LIFECYCLE TEST ===")

with client.websocket_connect("/ws/chat") as ws:
    print("CONNECTED = YES")

    request = {"message": "hello"}
    ws.send_json(request)
    print("SENT =", request)

    task_id = None
    deadline = time.time() + 30

    while time.time() < deadline:
        try:
            response = ws.receive_json()
            print("RECEIVED =", json.dumps(response, ensure_ascii=False))

            correlation = response.get("correlation") or {}
            current_task_id = correlation.get("task_id")

            if current_task_id:
                if task_id is None:
                    task_id = current_task_id
                    print("TASK_ID =", task_id)

                if current_task_id != task_id:
                    print("IGNORED OTHER TASK =", current_task_id)
                    continue

            state = response.get("state")

            if state in {"COMPLETED", "FAILED"}:
                print("=== TERMINAL STATE ===")
                print("TASK_ID =", task_id)
                print("STATE =", state)

                if state == "COMPLETED":
                    print("RESULT =", response)
                else:
                    print("FAILURE =", response)

                break

        except Exception as e:
            print("RECEIVE ERROR =", type(e).__name__, str(e))
            break
    else:
        print("=== TIMEOUT ===")
        print("TASK_ID =", task_id)
